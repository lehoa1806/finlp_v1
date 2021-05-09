from machine.postgres_batch_insert import PostgresBatchInsert
from workflow.consumer import Consumer
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer
from workflow.task import Task

from .scraper.vndirect_scraper import VnDirectScraper
from .warrant_getting_stage import WarrantGettingStage
from .warrant_scheduling_stage import WarrantSchedulingStage


class WarrantScraperTask(Task):
    def __init__(
        self,
        headless: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.headless = headless

    @property
    def consumer(self) -> Consumer:
        return PostgresBatchInsert(
            table_name='vietnam_warrants',
            batch_size=100,
        )

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=WarrantSchedulingStage()
        ).add_stage(
            stage=WarrantGettingStage(
                scraper=VnDirectScraper(headless=False, timeout=15),
            )
        )

    @property
    def producer(self):
        return SingleItemProducer({})

    @classmethod
    def process_task(
        cls,
        headless: bool = False,
        **kwargs,
    ) -> None:
        cls(headless=headless, **kwargs).main()
