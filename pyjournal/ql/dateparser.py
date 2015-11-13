from datetime import datetime
from ql.parser import ParseValidationError


def parse_str_date(date_str):
    formats = [_fn_1, _fn_2, _fn_3, _fn_4, _fn_5, _fn_6, _fn_7]
    for fn in formats:
        try:
            return fn(date_str)
        except ValueError:
            continue
    raise ParseValidationError('Could not parse date string')


def _fn_1(date_str):
    """Only hour e.g. 20:15"""
    now = datetime.now()
    r = datetime.strptime(date_str, '%H:%M')
    r = datetime(now.year, now.month, now.day, r.hour, r.minute)
    return r


def _fn_2(date_str):
    """Format dd/mm/yyyy ; dd-mm-yyyy ; dd mm yyyy ; mm dd, yyyy"""
    formats = ['%d/%m/%Y', '%d-%m-%Y',
               '%d/%b/%Y', '%d-%b-%Y', '%d %b %Y', '%b %d, %Y',
               '%d/%B/%Y', '%d-%B-%Y', '%d %B %Y', '%B %d, %Y']
    for _format in formats:
        try:
            r = datetime.strptime(date_str, _format)
            return datetime(r.year, r.month, r.day, 18, 0)
        except ValueError:
            continue
    raise ValueError


def _fn_3(date_str):
    """Format dd mm; mm dd"""
    now = datetime.now()
    formats = ['%d %b', '%b %d', '%d %B', '%B %d']
    for _format in formats:
        try:
            r = datetime.strptime(date_str, _format)
            return datetime(now.year, r.month, r.day, 18, 0)
        except ValueError:
            continue
    raise ValueError


def _fn_4(date_str):
    """Datetime e.g. 20:34 22/03/2017"""
    r = datetime.strptime(date_str, '%H:%M %d/%m/%Y')
    return r


def _fn_5(date_str):
    """Datetime e.g. 20:34 22/Oct/2017"""
    r = datetime.strptime(date_str, '%H:%M %d/%b/%Y')
    return r


def _fn_6(date_str):
    """Datetime e.g. 20:34 October 22 2017"""
    r = datetime.strptime(date_str, '%H:%M %B %d %Y')
    return r


def _fn_7(date_str):
    """Today or Yesterday"""
    now = datetime.now()
    _str = date_str.lower()
    if _str == 'today':
        r = datetime(now.year, now.month, now.day, 18, 0)
    elif _str == 'yesterday':
        r = datetime(now.year, now.month, now.day - 1, 18, 0)
    else:
        raise ValueError
    return r
