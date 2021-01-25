import re
from datetime import datetime
from enum import Enum

import pytz

MY_TIMEZONE = 'Asia/Kuala_Lumpur'
VN_TIMEZONE = 'Asia/Ho_Chi_Minh'
NEWS_QUERY = '''
SELECT
  news_id,
  news_detail->'time' AS time,
  news_name AS title,
  (
    CASE
     WHEN CAST(news_detail->'category' AS VARCHAR) IS NULL THEN ''
     ELSE trim('"' FROM CAST(news_detail->'category' AS VARCHAR))
    END
  ) AS category,
  news_source AS source,
  news_url AS url,
  news_detail->'content' AS content
FROM
  {table}
ORDER BY
  news_date DESC;
'''


class Subscription(Enum):
    EXCLUDE = -1
    HOLDING = 0
    HOT = 1
    TOTAL = 100
    ANNOUNCEMENT = 1000


class TimeShift:
    WORKING = 0
    NIGHT = 1
    WEEKEND = 2
    REST = 3

    def __init__(self, timezone: str):
        self.timezone = pytz.timezone(timezone)

    @property
    def current(self) -> int:
        """
        08:00 -- 19:00: WORKING
        19:00 -- 22:00: NIGHT
        22:00 -- 00:00 -- 08:00: REST
        Priority order: WORKING -> NIGHT -> WEEKEND -> REST
        """
        utcnow = datetime.utcnow()
        now = utcnow.replace(tzinfo=pytz.utc).astimezone(self.timezone)
        if now.hour >= 22 or now.hour <= 8:
            return self.REST
        if now.weekday() in [5, 6]:
            return self.WEEKEND
        elif now.hour >= 19:
            return self.NIGHT
        return self.WORKING


def get_time(
    time_string: str,
    time_format: str,
    timezone: str,
    sub_format: str = None
) -> datetime:
    def add_zero_pad(matched_int):
        return '0{}'.format(matched_int.group(0))

    time = re.sub(r'\b\d\b', add_zero_pad, time_string)
    local = pytz.timezone(timezone)
    try:
        return local.localize(datetime.strptime(time, time_format))
    except ValueError:
        if sub_format:
            return local.localize(datetime.strptime(time, sub_format))
    return local.localize(datetime.utcnow())


def get_local_date(date_string: str, timezone: str) -> datetime:
    local = pytz.timezone(timezone)
    try:
        return local.localize(datetime.strptime(date_string, '%Y-%m-%d'))
    except ValueError:
        try:
            return local.localize(
                datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            )
        except ValueError as error:
            raise ValueError(
                "Invalid date format({}), should be YYYY-MM-DD or "
                "YYYY-MM-DD HH:MM:SS".format(str(error))
            )
