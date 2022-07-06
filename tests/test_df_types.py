import pandas as pd
import pandas.api.types as ptypes


def testDataTypes():

    df = pd.read_csv('../outputFiles/merge.csv')

    df['XR'] = df['XR'].astype('Int64', errors='ignore')

    print(df['XR'].dtype)

    # check if the XR column is of Int64 type 
    assert ptypes.is_int64_dtype(df['XR'])