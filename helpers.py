from dictionaries import month_numbers
import re
import datetime


def format_date(t):

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


def format_date_source2(t):

    t = t.decode('utf-8')
    t = "".join(t.split())

    match0 = re.compile('(\d+)-(\d+)(\w+)').match(t)

    if t == '':
        return t
    for m in month_numbers.keys():
        if match0:
            if m in match0.group(3).lower():
                m0 = get_month_number(match0.group(3))
                if int(match0.group(1)) > int(match0.group(2)):
                    m0 = '{}'.format(int(m0) - 1)
                s = '{}-{}-{}-{}-{}-{}'.format(
                    '2018',
                    get_two_digit_month(m0),
                    get_two_digit_day(match0.group(1)),
                    '2018',
                    get_month_number(match0.group(3)),
                    get_two_digit_day(match0.group(2)))
                return s


def format_date_and_location_source3(t):

    match0 = re.compile('(\d+)\s\w+\s(\d+)\s(\w+)\s\w+\s(\D+)').search(t)
    match1 = re.compile(r'(\d+)\s(\w+)\s\w+\s(\d+)\s(\w+)\s\w+\s(\D+)').search(t)
    match2 = re.compile(r'(\d+)\s(\w+)\s\w+\s(\D+)').match(t)

    if t == '':
        return t
    for m in month_numbers.keys():
        if match0:
            if m in match0.group(3).lower():
                return {
                    'date':
                        '{}-{}-{}-{}-{}-{}'.format(
                    '2018',
                    get_month_number(match0.group(3)),
                    get_two_digit_day(match0.group(1)),
                    '2018',
                    get_month_number(match0.group(3)),
                    get_two_digit_day(match0.group(2))),
                    'location': match0.group(4)
                }
        if match1:
            if m in match1.group(2).lower():
                return{
                    'date':
                        '{}-{}-{}-{}-{}-{}'.format(
                    '2018',
                    get_month_number(match1.group(2)),
                    get_two_digit_day(match1.group(1)),
                    '2018',
                    get_month_number(match1.group(4)),
                    get_two_digit_day(match1.group(3))),
                    'location': match1.group(5)
                }
        if match2:
            if m in match2.group(2).lower():
                return{
                    'date':
                        '{}-{}-{}-{}-{}-{}'.format(
                    '2018',
                    get_month_number(match2.group(2)),
                    get_two_digit_day(match2.group(1)),
                    '2018',
                    get_month_number(match2.group(2)),
                    get_two_digit_day(match2.group(1))),
                    'location': match2.group(3)
                }


def format_date_source_4(t):

    match0 = re.compile('(\d+) ([а-яА-Я]+) (\d+)').match(t)
    match1 = re.compile('(\d+) -  (\d+) ([а-яА-Я]+) (\d+)').match(t)
    match2 = re.compile('(\d+) - (\d+) ([а-яА-Я]+) (\d+)').match(t)

    if t == '':
        return t
    for m in month_numbers.keys():
        if match0:
            if m in match0.group(2).lower():
                s = '{}-{}-{}-{}-{}-{}'.format(
                    '2018',
                    get_two_digit_month(get_month_number(match0.group(2))),
                    get_two_digit_day(match0.group(1)),
                    '2018',
                    get_two_digit_month(get_month_number(match0.group(2))),
                    get_two_digit_day(match0.group(1)))
                return s
        if match1:
            if m in match1.group(3).lower():
                s = '{}-{}-{}-{}-{}-{}'.format(
                    '2018',
                    get_two_digit_month(get_month_number(match1.group(3))),
                    get_two_digit_day(match1.group(1)),
                    '2018',
                    get_two_digit_month(get_month_number(match1.group(3))),
                    get_two_digit_day(match1.group(2)))
                return s
        if match2:
            if m in match2.group(3).lower():
                s = '{}-{}-{}-{}-{}-{}'.format(
                    '2018',
                    get_two_digit_month(get_month_number(match2.group(3))),
                    get_two_digit_day(match2.group(1)),
                    '2018',
                    get_two_digit_month(get_month_number(match2.group(3))),
                    get_two_digit_day(match2.group(2)))
                return s


def get_month_number(m):
    return month_numbers.get(m.lower(), '')


def get_two_digit_day(d):
    int_d = int(d)
    temp = datetime.date(2017, 10, int_d)
    return '{:02d}'.format(temp.day)


def get_two_digit_month(m):
    int_m = int(m)
    temp = datetime.date(2017, int_m, 1)
    return '{:02d}'.format(temp.month)


def get_list_by_list_object_key(items, key):
    result_list = []
    for item in items:
        result_list.append(item[key])

    return result_list

