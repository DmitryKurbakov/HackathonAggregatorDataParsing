from dictionaries import month_numbers
import re
import datetime


def format_date_source_0(t):

    t = t.decode('utf-8')
    m0 = ''
    m1 = ''

    match0 = re.compile('(\w+) (\d+)  (\d+), (\d{4})').match(t)
    match1 = re.compile('^(\w+) (\d+), (\d{4})').match(t)
    match2 = re.compile('(\w+) (\d+)  (\w+) (\d+), (\d{4})').match(t)

    if t == '':
        return t

    for m in month_numbers.keys():
        if match0:
            if m in match0.group(1).lower():
                return '{}-{}-{}-{}-{}-{}'.format(
                    match0.group(4),
                    get_month_number(match0.group(1)),
                    get_two_digit_day(match0.group(2)),
                    match0.group(4),
                    get_month_number(match0.group(1)),
                    get_two_digit_day(match0.group(3)))
        if match1:
            if m in match1.group(1).lower():
                return '{}-{}-{}-{}-{}-{}'.format(
                    match1.group(3),
                    get_month_number(match1.group(1)),
                    get_two_digit_day(match1.group(2)),
                    match1.group(3),
                    get_month_number(match1.group(1)),
                    get_two_digit_day(match1.group(2)))
        if match2:
            if m in match2.group(1).lower():
                m0 = get_month_number(match2.group(1))
            if m in match2.group(3).lower():
                m1 = get_month_number(match2.group(3))
            if m0 != '' and m1 != '':
                return '{}-{}-{}-{}-{}-{}'.format(
                    match2.group(5),
                    get_month_number(match2.group(1)),
                    get_two_digit_day(match2.group(2)),
                    match2.group(5),
                    get_month_number(match2.group(3)),
                    get_two_digit_day(match2.group(4)))


def get_month_number(m):
    return month_numbers.get(m.lower(), '')


def get_two_digit_day(d):
    temp = datetime.date(2017, 10, int(d))
    return '{:02d}'.format(temp.day)


# a = format_date_source_0('Apr 6  7, 2018')
# b = format_date_source_0('Apr 13  14, 2018')
# c = format_date_source_0('Apr 7, 2018')
# d = format_date_source_0('Mar 19  Jun 1, 2018')
# i = 0