import re
from datetime import datetime
from enum import Enum

import pytz

MY_TIMEZONE = 'Asia/Kuala_Lumpur'
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
        return local.localize(datetime.strptime(time, sub_format))


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
