import pandas as pd 
import json
from DataSync.pyAlchemy.connector import connectToSQLServer
from DataSync.compareCSV.compare import compareSEIS

def getDroppedSEISIDs(seisFile):
    # create 1st snapshot csv from dataframe
    seisFile.to_csv('outputFiles/seisFile_snapshot.csv', index=False)

    # drop rows where District ID is not numeric or blank
    seisFileFiltered = seisFile[ pd.to_numeric( seisFile['District ID'], errors='coerce' ).notnull() ]

    # create 2nd csv snapshot 
    seisFileFiltered.to_csv('outputFiles/seisFile_filtered.csv', index=False)

    # compare 1st and 2nd snapshots to find dropped records 
    compareSEIS( "outputFiles/seisFile_snapshot.csv", "outputFiles/seisFile_filtered.csv", "District ID", "District ID" )



def getListOfSpEdIDs(seisIDList):
    # join list to a string => for use in SQL query
    values = ','.join(str(i) for i in seisIDList)

    return values



# returns index based on whether colume == value 
def getIndex( df, column, value ): 
    '''
    Takes Dataframe, Column name, and Value to be searched \n
    Returns index of the row
    '''
    # use .toList() to resturn list
    return df.loc[df[column] == value].index[0]



def replaceVal(df1 , col1, val1, df2, col2, val2):
    '''
    df1 = Aeries output dataframe
    col1 = column of the value you want to replace
    val1 = ID of student in Aeries file
    
    df2 = SEIS output dataframe
    col2 = column of the value you want use
    val2 = ID of student in SEIS file
    '''
    # get ID's row index
    indexA = getIndex( df1, 'ID', val1 )

    # get ID's row index
    indexB = getIndex( df2, 'District ID', val2 )

    # replace Aeries output df value with seisFile df value
    df1.at[indexA, col1] = df2.at[indexB, col2]

    return df1



def replaceValWithMapping(df1, col1, val1, df2, col2, val2):
    '''
    df1 = Aeries output dataframe
    col1 = column of the value you want to replace
    val1 = ID of student in Aeries file
    
    df2 = SEIS output dataframe 
    col2 = column of the value you want use
    val2 = ID of student in SEIS file
    '''

    # get ID's row index
    indexA = getIndex( df1, 'ID', val1 )

    # get ID's row index
    indexB = getIndex( df2, 'District ID', val2 )


    if col2 == "School Type (Attendance School)":
        # open json mapping file 
        jsonFile = open('./mappings/school_type_mapping.json')

        # convert json to python compatible format
        data = json.load(jsonFile)

        try:
            # replace Aeries output df value with mapped value 
            df1.at[indexA, col1] = data[ df2.at[indexB, col2].strip() ]
        except Exception as e:
            print("Error with school type mapping")
            print(e)
            print(val2)
            quit()

    elif col2 == "Percent IN Regular Class":
        #open json mapping file
        jsonFile = open('./mappings/percent_in_regular_class_mapping.json')

        # convert json to python compatible format
        data = json.load(jsonFile)

        # check if SEIS value is not NaN (including blank)
        if pd.isna( df2.at[indexB, col2] ) == False :
            value = int(df2.at[indexB, col2])

            if value >= 80:
                df1.at[indexA, col1] = data['Equal to or Greater than 80 percent'] 
            elif 40 <= value <= 79:
                df1.at[indexA, col1] = data['40 percent to 79 percent']
            elif value < 40:
                df1.at[indexA, col1] = data['Less than 40 percent']
            else:
                print("Error with percent in regular class mapping")
                print(e)
                print(val2)
                quit()

    elif col2 == "Case Manager":
        # get case manager's email value
        cmEmail = df2.at[indexB, 'Case Manager Email']

        # if case manager email not NaN and not blank 
        if pd.isna(cmEmail) == False and len(cmEmail.strip()):

            # split email into prefix and domain
            emailPieces = cmEmail.split('@')

            # get email prefix 
            prefix = emailPieces[0]

            # get domain
            domain = emailPieces[1]

            if domain == 'tustin.k12.ca.us':

                cnxn = connectToSQLServer()

                try:
                    # query returns case manager's STAFF ID
                    query = f'SELECT TOP 1 UGN.SID FROM UGN WHERE UGN.UN = \'{prefix}\';'

                    df = pd.read_sql_query(query, con=cnxn)

                    # check that sql returns at least 1 value
                    if len(df['SID']) > 0:
                        df1.at[indexA, col1] = df['SID'][0]

                    cnxn.dispose()
                except Exception as e:
                    print("Error with case manager mapping")
                    print(e)
                    print(val2)
                    quit()

    elif col2 == "Plan Type  (Edu Plan for SpEd Svcs)":
        #open json mapping file
        jsonFile = open('./mappings/education_plan_type_mapping.json')

        # convert json to python compatible format
        data = json.load(jsonFile)

        # replace nan with ''
        df2[col2] = df2[col2].fillna('') 

        try:
            if df2.at[indexB, col2] != '':
                # replace Aeries output df value with mapped value 
                df1.at[indexA, col1] = data[ df2.at[indexB, col2].strip() ]
        except Exception as e:
            print("Error with education plan type mapping")
            print(e)
            print(val2)
            quit()

    else:
        return df1 

    return df1
