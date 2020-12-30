import datetime
import time


def datetime2datedict(d):
    rd = dict()
    rd["year"] = d.year
    rd["month"] = d.month
    rd["day"] = d.day
    rd["hour"] = d.hour
    rd["minute"] = d.minute
    rd["second"] = d.second
    return rd


def ymd2stamp(y, m, d):
    s = "%d %d %d" % (y, m, d)
    return int(time.mktime(datetime.datetime.strptime(s, "%Y %m %d").timetuple()))


def datedict2stamp(d):
    if "hour" in d:
        hour = d["hour"]
    else:
        hour = 0
    if "minute" in d:
        minute = d["minute"]
    else:
        minute = 0
    if "second" in d:
        second = d["second"]
    else:
        second = 0

    s = "%d %d %d %d %d %d" % (d["year"], d["month"], d["day"], hour, minute, second)
    return int(time.mktime(datetime.datetime.strptime(s, "%Y %m %d %H %M %S").timetuple()))


def get_today_ymd():
    ymd = datetime.date.today().strftime("%Y%m%d")
    return ymd


def get_yesterday_ymd():
    ymd = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    return ymd


def stamp2datedict(stamp):
    d = datetime.datetime.fromtimestamp(stamp)
    return datetime2datedict(d)


def get_now_datedict():
    now = datetime.datetime.now()
    return datetime2datedict(now)


def test():
    now_dict = get_now_datedict()
    print(now_dict)

    stamp = datedict2stamp(now_dict)
    print(stamp)

    now_dict2 = stamp2datedict(stamp)
    print(now_dict2)


if __name__ == "__main__":
    test()
