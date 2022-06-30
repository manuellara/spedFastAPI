from DataSync.pyAlchemy.connector import connectToSQLServer

def test_cnxn_engine():
    cnxn = connectToSQLServer()

    # test if engine gets created
    assert cnxn != None 