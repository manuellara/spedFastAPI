from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def connectToSQLServer():

    sqlDriver='ODBC+Driver+17+for+SQL+Server'
    sqlServer = os.getenv('sqlServer')
    sqlDatabase = os.getenv('sqlDatabase')
    sqlSA = os.getenv('sqlSA')
    sqlSAPass = os.getenv('sqlSAPass')

    try:
        # engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server') # run locally
        engine = create_engine(f'mssql://{sqlSA}:{sqlSAPass}@{sqlServer}/{sqlDatabase}?driver={sqlDriver}')
        return engine
    except Exception as e:
        print(e)
        print("Something went wrong while trying to connect to SQL Server")
        return None