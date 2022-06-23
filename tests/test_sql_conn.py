from DataSync.pyAlchemy.connector import connectToSQLServer

def test_cnxn_engine():
    cnxn = connectToSQLServer()

    # test engine gets created
    assert cnxn != None 