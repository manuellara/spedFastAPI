from sqlalchemy import create_engine
import os

def connectToSQLServer():

    sqlDriver='ODBC+Driver+17+for+SQL+Server'
    sqlServer = os.environ['sqlServer']
    sqlDatabase = os.environ['sqlDatabase']
    sqlSA = os.environ['sqlSA']
    sqlSAPass = os.environ['sqlSAPass']

    try:
        # engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server') # run locally
        engine = create_engine(f'mssql://{sqlSA}:{sqlSAPass}@{sqlServer}/{sqlDatabase}?driver={sqlDriver}')
        return engine
    except Exception as e:
        print(e)
        print("Something went wrong while trying to connect to SQL Server")
        return None