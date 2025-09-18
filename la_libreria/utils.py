def get_date():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d") 

def get_ts():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def substract_date(date_str,interval="d",amount=1, date_format="%Y-%m-%d"):
    from datetime import datetime, timedelta
    date_obj = datetime.strptime(date_str, date_format)
    if interval == "d":
        prev = date_obj - timedelta(days=amount)
    if interval == "m":
        prev = date_obj - timedelta(months=amount)
    if interval == "y":
        prev = date_obj - timedelta(years=amount)
    return prev.strftime(date_format)

def parse_query(filepath,replacemment_dict={}):
    import sys
    fp = filepath
    rd = replacement_dict
    try:
        q = open(fp,"r").read()
        for k,v in rd.items():
            q = q.replace(k,v)
        return q
    except Exception as e:
        sys.exit(e)
