def get_date():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d") 

def get_ts():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
