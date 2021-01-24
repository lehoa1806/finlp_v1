import subprocess
from datetime import datetime

from news.utils.filter import Filter
from workflow.consumer import Consumer
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer
from workflow.task import Task


class ScraperTask(Task):
    def __init__(
        self,
        ft: Filter,
        start_time: datetime,
        end_time: datetime,
        headless: bool,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.filter = ft
        self.start_time = start_time
        self.end_time = end_time
        self.headless = headless

    @property
    def consumer(self) -> Consumer:
        raise NotImplementedError

    @property
    def pipeline(self) -> Pipeline:
        raise NotImplementedError

    @property
    def producer(self):
        return SingleItemProducer({
            'start_time': self.start_time,
            'end_time': self.end_time,
        })

    @classmethod
    def process_task(
        cls,
        ft: Filter,
        start_time: datetime,
        end_time: datetime,
        headless: bool,
        **kwargs,
    ) -> None:
        cls(ft=ft, start_time=start_time, end_time=end_time,
            headless=headless, **kwargs).main()

    def teardown(self) -> None:
        cmd = 'pkill -9 chrome'
        subprocess.check_call(cmd.split())
        cmd = 'pkill -9 chromedriver'
        subprocess.check_call(cmd.split())
        super().teardown()
