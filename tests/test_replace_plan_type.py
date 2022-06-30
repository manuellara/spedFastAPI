from DataSync.pandasFunc.pandasOperations import replaceValWithMapping
import pandas as pd
import os 


def test_replace_plan_type():
    '''
    df1 = Aeries output dataframe
    col1 = column of the value you want to replace
    val1 = ID of student in Aeries file
    
    df2 = SEIS output dataframe 
    col2 = column of the value you want use
    val2 = ID of student in SEIS file
    '''

    # create aeries df
    aeries_cse_df = pd.read_csv("../outputFiles/aeries_cse_output.csv")

    # create seis df
    seis_fitered_df = pd.read_csv("../outputFiles/seisFile_filtered.csv")

    # run function from the root directory (instead of tests directory)
    os.chdir(r'C:\\Users\\malara\\Desktop\\spedFastAPI')

    df = replaceValWithMapping(aeries_cse_df, "PT", int(46000607), seis_fitered_df, "Plan Type  (Edu Plan for SpEd Svcs)", int(46000607))

    assert df.all