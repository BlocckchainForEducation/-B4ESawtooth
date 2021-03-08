import datetime
import time


def get_time():
    dts = datetime.datetime.utcnow()
    return round(time.mktime(dts.timetuple()) + dts.microsecond / 1e6)


def add_years(d, years):
    try:
        # Return same day of the current year
        return d.replace(year=d.year + years)
    except ValueError:
        # If not same day, it will return other, i.e.  February 29 to March 1 etc.
        return d + (datetime.date(d.year + years, 1, 1) - datetime.date(d.year, 1, 1))


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def to_time_stamp(date_time):
    return datetime.datetime.timestamp(date_time)

print(timestamp_to_datetime(int("24345435")).year)

print(2 < int("3"))