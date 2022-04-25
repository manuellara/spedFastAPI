# import pyodbc
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
import os

def connectToSQLServer():

    server = os.environ.get("server")
    database = os.environ.get("database")
    username = os.environ.get("username")
    password = os.environ.get("password")

    try:
        # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';Trusted_Connection=yes;')
        engine = create_engine(f"mssql+pyodbc://{username}:{password}@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server")
        # print("Connected to SQL Server successfully")
        return engine
    except:
        print("Something went wrong while tring to connect to SQL Server")
        return None
    