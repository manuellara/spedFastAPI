from datetime import datetime

def getDate():
    date = datetime.today()
    today = date.strftime('%Y-%m-%d')

    return today