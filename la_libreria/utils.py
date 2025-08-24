def get_date():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d") 

def get_ts():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def substract_date(date_str,interval="d",amount=1, date_format="%Y-%m-%d"):
    from datetime import datetime, timedelta
    date_obj = datetime.strptime(s, date_format)
    if interval == "d":
        prev = date_obj - timedelta(days=amount)
    if interval == "m":
        prev = date_obj - timedelta(months=amount)
    if interval == "y":
        prev = date_obj - timedelta(years=amount)
    return prev.strftime(date_format)
