
import time
import datetime

def format_time(timestamp):

    t = datetime.datetime.fromtimestamp(timestamp)

    "6/03/2020 - 12:34"
    return "{}/{}/{} - {}:{}".format(t.day, t.month, t.year, t.hour, t.minute)