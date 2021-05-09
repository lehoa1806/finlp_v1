from contextlib import contextmanager
from time import sleep
from typing import Generator

from utils.dynamodb import Database

from .tracker import Tracker


class UrlTracker(Tracker):
    def __init__(self, database: Database, reset: int = 5) -> None:
        super().__init__(database)
        self.reset = reset
        self.continuous: int = 0

    @property
    def tracker(self):
        return 'url'

    @contextmanager
    def track(self, url: str) -> Generator:
        if self.get(key=url):
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
                self.save({self.pkey: url})
