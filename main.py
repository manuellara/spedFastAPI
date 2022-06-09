from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
import json
from fastapi.responses import FileResponse
from DataSync.compareCSV.compare import compareCSV
from DataSync.pyAlchemy.connector import connectToSQLServer
from DataSync.pandasFunc.pandasOperations import getDroppedSEISIDs, replaceVal, getListOfSpEdIDs, replaceValWithMapping

app = FastAPI()

@app.get("/health", tags=["Health"])
async def health():
    return {"message": "SpEd FastAPI is running!"}


@app.post("/upload_csv", tags=["Upload SEIS CSV"])
async def upload_csv(input: UploadFile = File(...)):

    try:
        # read CSV file into dataframe 
        seisFile = pd.read_csv(input.file)
    except Exception as e:
        print("unable to convert input file to pandas df")
        print(e)
        raise HTTPException(status_code=415, detail="Please upload a file with the extention .CSV")

    # creates 3 files:
        # seisFile_snapshot.csv: initial snapshot in df format
        # seisFile_filtered.csv: District ID is filtered and only numeric values are kept
        # compare_SEIS.json: snapshot.csv and filtered.csv are compared and dropped District IDs are listed 
    getDroppedSEISIDs(seisFile)

    # read in the filtered CSV (District ID cleaned up)
    seisFile = pd.read_csv("outputFiles/seisFile_filtered.csv")

    # convert District ID into int data type
    seisFile['District ID'] = seisFile['District ID'].apply(int)


    try:
        # convert 'Disability 1 Code' and 'Disability 2 Code' to integer type
        colsToInt = ['Disability 1 Code', 'Disability 2 Code']
        for i in colsToInt:
            seisFile[i] = pd.to_numeric(seisFile[i],errors='coerce').astype(pd.Int64Dtype())
    except Exception as e:
        print("unable to convert 'Disability 1 Code' and 'Disability 2 Code' to integer type")
        print(e)
        raise HTTPException(status_code=500, detail="Could not convert Disability codes")

    # returns SpEd IDs as str for use with SQL query
    values = getListOfSpEdIDs(seisFile['District ID'].tolist())

    # initialize empty df for 'Aeries output.csv'
    df = pd.DataFrame()

    # query SQL Server 
    try:
        cnxn = connectToSQLServer()

        if cnxn == None:
            raise HTTPException(status_code=500, detail="SQL Server Connection string returned None")
        
        # build query
        query = f'SELECT * FROM CSE WHERE CSE.ID IN ({values});'

        # execute query
        # print("Running SQL query...")
        df = pd.read_sql_query(query, con=cnxn)

        # kill SQL Server connection
        # print("Success...closing connection to SQL Server")
        cnxn.dispose()            
    except Exception as e:
        print("Something went wrong trying to query SQL Server: ", e)
        print(e)
        raise HTTPException(status_code=500, detail="Could not execute SQL query")


    try:
        # convert CSE date fields to a readable format mm/dd/yyyy
        colsToDate = ['ED','LI','LA','XD','AD','TA','DT','IE'] # removed 'DTS' from the list because it's generated by SQL Server on input
        for i in colsToDate:
            df[i] = pd.to_datetime(df[i]).dt.strftime('%m/%d/%Y')
    except Exception as e:
        print(f'Something went wrong trying to convert Aeries datetime field to readable format: CSE.{i}')
        print(e)
        raise HTTPException(status_code=500, detail=f'Could not convert Aeries CSE.{i}: {e}')


    # creates 1 file:
        # aeries_cse_output.csv: Aeries CSE table snapshot 
    df.to_csv("outputFiles/aeries_cse_output.csv", index = False)


    # opens mappings json file
    jsonFile = open('mappings/attribute_mapping.json')

    # converts json to python dict (i.e. python readble)
    data = json.load(jsonFile)


    # process replace values for each ID for Aeries output df
    for id in df['ID']:
        for i in data['mapping']:

            if i['needs_mapping'] == True:
                try:
                    ## replace value function for attributes that need mapping
                    df = replaceValWithMapping( df, i['Aeries'], id, seisFile, i['SEIS'], id )
                except Exception as e:
                    print(e)
                    print(id)
                    raise HTTPException(status_code=500, detail="Problem with value that needs mapping")
            else:
                try:
                    ## replace value function for attributes that do not need mapping
                    df = replaceVal( df, i['Aeries'], id, seisFile, i['SEIS'], id )
                except Exception as e:
                    print(e)
                    print(id)
                    raise HTTPException(status_code=500, detail="Problem with value that does not needs mapping")


    # creates 1 file:
        # merge.csv: outfile from inserting SEIS data values into Aeries CSE table
    df.to_csv("outputFiles/merge.csv", index=False)

    # creates 1 file:
        # compare_data.json: compares the data diffrences with initial Aeries CSE snapshot and merged data
    compareCSV("outputFiles/aeries_cse_output.csv", "outputFiles/merge.csv", "ID", "ID")

    # returns difference as response
    jsonCompare = open('outputFiles/compare_data.json')
    data = json.load(jsonCompare)

    #return FileResponse('outputFiles/merge.csv', media_type='text/csv',filename='outputFiles/merge.csv')
    # return data
    return {"message": f"{input.filename} processed successfully!"}


@app.post("/get_merged", tags=["Get Merged CSV"])
async def get_merged():
    return FileResponse('outputFiles/merge.csv', media_type='text/csv', filename='outputFiles/merge.csv')


@app.post("/get_diff", tags=["Get Differences JSON"])
async def get_diff():
    return FileResponse('outputFiles/compare_data.json', media_type='application/json', filename='outputFiles/compare_data.json')


@app.post("/get_bad_seis", tags=["Get bad SEIS JSON"])
async def get_bad_seis():
    return FileResponse('outputFiles/compare_SEIS.json', media_type='application/json', filename='outputFiles/compare_SEIS.json')