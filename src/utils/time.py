import datetime
import time


# noinspection PyShadowingBuiltins
def to_timestamp(s: str, format: str):
    return time.mktime(datetime.datetime.strptime(s, format).timetuple())


# noinspection PyShadowingBuiltins
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)
