import re
import datetime
import pytz
def parseDatetime(date_str):

    if str(date_str).find("sec") != -1:
        date_str=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(seconds=int(re.sub('\D', '', date_str)))
    elif str(date_str).find("min") != -1:
        date_str=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(minutes=int(re.sub('\D', '', date_str)))
    elif str(date_str).find("hour") != -1:
        date_str=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(hours=int(re.sub('\D', '', date_str)))
    elif str(date_str).find("day") != -1:
        date_str=datetime.datetime.now().astimezone(pytz.utc)-datetime.timedelta(days=int(re.sub('\D', '', date_str)))

    return date_str