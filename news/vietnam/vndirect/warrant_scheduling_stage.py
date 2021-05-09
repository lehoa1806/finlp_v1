import logging
from datetime import datetime
from typing import Dict, Iterator

import pytz

from news.utils.common import VN_TIMEZONE
from workflow.stage import Stage

TIME_FORMAT = '%-d/%-m/%Y %H:%M:%S'


class WarrantSchedulingStage(Stage):
    def process(self, item: Dict) -> Iterator[Dict]:
        utcnow = datetime.utcnow()
        local_timezone = pytz.timezone(VN_TIMEZONE)
        now = utcnow.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        if now.weekday() in [5, 6]:
            logging.info('Weekend -- stop working and enjoy the sleep!!!')
            return
        start_morning = now.replace(hour=8, minute=55, second=0)
        end_morning = now.replace(hour=11, minute=30, second=0)
        start_evening = now.replace(hour=12, minute=55, second=0)
        end_evening = now.replace(hour=15, minute=0, second=0)
        if now < start_morning or now > end_evening:
            logging.info('Non-working time -- back to sleep')
            return
        elif end_morning < now < start_evening:
            logging.info('Lunch time -- let\'s eat')
            return
        else:
            yield {}
