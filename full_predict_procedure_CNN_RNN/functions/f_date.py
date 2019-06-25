import datetime


def daterange(date1, date2):
    """
    :param date1: start date
    :param date2: end date
    :return: a list of date
    """
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + datetime.timedelta(n)


def date_format(date):

    list_date = date.split("-")
    year, month, day = list_date[0], list_date[1], list_date[2]

    return datetime.date(int(year), int(month), int(day))


def add_date(date, day):

    formated_date = date_format(date)
    date_add_days = formated_date + datetime.timedelta(days=day)

    return date_add_days


def minus_date(date, day):

    formated_date = date_format(date)
    date_add_days = formated_date - datetime.timedelta(days=day)

    return date_add_days

"""
# convert date format to string
import datetime
t = datetime.datetime(2012, 2, 23, 0, 0)
t.strftime('%m/%d/%Y')
"""
