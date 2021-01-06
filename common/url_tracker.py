from contextlib import contextmanager
from time import sleep
from typing import Any, Dict, Generator, Optional

from aws_apis.dynamodb.database import Database


class UrlTracker:
    def __init__(self, database: Database, reset: int = 5) -> None:
        self.table = database.get_url_tracking_table()
        self.reset = reset
        self.continuous: int = 0

    def get(self, url: str) -> Optional[Dict[str, Any]]:
        return self.table.get_item(partition_key=url)

    def save(self, url: str) -> None:
        self.table.put_item({'url': url})

    @contextmanager
    def track(self, url: str) -> Generator:
        if self.get(url):
            self.continuous += 1
            sleep(0.2)
            if self.continuous >= self.reset:
                yield None
            else:
                yield ''
        else:
            try:
                self.continuous = 0
                yield url
            finally:
                self.save(url)
