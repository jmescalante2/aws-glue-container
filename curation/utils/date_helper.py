from datetime import datetime, timezone

from dateutil import parser


def get_current_utc_datetime():
    """
    Returns current time as timezone aware datetime in UTC.

    Sample:
    datetime.datetime(2023, 6, 12, 8, 58, 37, 747133, tzinfo=datetime.timezone.utc)
    """
    return datetime.now(timezone.utc)


def datetime_to_str(date):
    """
    Converts a datetime to string representation (with the same timezone awareness).

    This is used for simple storage of datetime as string.

    Sample:
    datetime.datetime(2023, 6, 12, 8, 58, 37, 747133, tzinfo=datetime.timezone.utc)
      => '2023-06-12 08:58:37.747133+00:00'
    """
    return str(date)


def str_to_datetime(string):
    """
    Converts a string representation to a datetime (with the same timezone awareness).

    This is used for simple interpretation of a stored datetime.

    Sample:
    '2023-06-12 08:58:37.747133+00:00'
      => datetime.datetime(2023, 6, 12, 8, 58, 37, 747133, tzinfo=tzutc())
    """
    return parser.parse(string)


def naive_utc_datetime_to_utc_datetime(date):
    """
    Converts a naive datetime in UTC to a timezone aware datetime in UTC.

    This is only used when you are forced to deal with a naive datetime that you
    know is UTC.

    Sample:
    datetime.datetime(2023, 6, 9, 8, 13, 33)
      => datetime.datetime(2023, 6, 9, 8, 13, 33, tzinfo=datetime.timezone.utc)
    """
    return date.replace(tzinfo=timezone.utc)


def datetime_diff_in_hours(d1, d2):
    """
    Gives difference in terms of hours.
    """
    return (d1 - d2).total_seconds() / 3600.0
