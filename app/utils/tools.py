import sys

from datetime import datetime, date


def is_win():
    """
    Returns whether we are running on Windows.
    :return: (Boolean) whether we are running on Mac Windows
    """
    return sys.platform.startswith('win')


def is_mac():
    """
    Returns whether we are running on Mac OSX.
    :return: (Boolean) whether we are running on Mac OSX
    """
    return sys.platform.startswith('darwin')


def get_date_string():
    """
    Returns a date string formatting as 'YYYY-MMDD-HHMM'.
    :return: (string) a date string formatting as 'YYYY-MMDD-HHMM'
    """
    # the year/month/day string, showing 'YYYY-MMDD'
    date_str = date.today().strftime("%Y-%m%d")
    # the hour/min string, showing 'HHMM'
    time_str = datetime.now().strftime("%H%M")
    return '{}-{}'.format(date_str, time_str)
