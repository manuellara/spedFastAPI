from datetime import datetime
from DataSync.pyDateTime.getDateTime import getDate


def test_date_format():
    # test if date is in year, month, day format e.g. '2022-06-09'
    assert getDate() == datetime.today().strftime('%Y-%m-%d') 
