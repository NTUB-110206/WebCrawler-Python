import re
import datetime
import pytz
def parseDatetime(date_str):
    date_str = str(date_str)
    date_str = date_str[date_str.find('|')+2:] if date_str.find('|')>0 else date_str
    if date_str.find("sec") != -1:
        date_str=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(seconds=int(re.sub('\D', '', date_str)))
    elif date_str.find("min") != -1:
        date_str=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(minutes=int(re.sub('\D', '', date_str)))
    elif date_str.find("hour") != -1:
        date_str=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(hours=int(re.sub('\D', '', date_str)))
    elif date_str.find("day") != -1:
        date_str=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(days=int(re.sub('\D', '', date_str)))
    else:
        date_str = str(mdy_to_ymd(date_str.replace(" ", "")))+' 00:00:00'
    return date_str

def mdy_to_ymd(d):
    return datetime.datetime.strptime(d, '%b%d,%Y').strftime('%Y-%m-%d')