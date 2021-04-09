from machine.postgres_batch_insert import PostgresBatchInsert
from workflow.consumer import Consumer
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer
from workflow.task import Task

from .scraper.vndirect_scraper import VnDirectScraper
from .warrant_getting_stage import WarrantGettingStage


class WarrantScraperTask(Task):
    def __init__(
        self,
        cool_down: int = 60,
        break_period: int = 3600,
        headless: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.headless = headless
        self.cool_down = cool_down
        self.break_period = break_period

    @property
    def consumer(self) -> Consumer:
        return PostgresBatchInsert(
            table_name='vietnam_warrants',
            batch_size=100,
        )

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=WarrantGettingStage(
                scraper=VnDirectScraper(headless=self.headless, timeout=15),
                cool_down=self.cool_down,
                break_period=self.break_period,
            )
        )

    @property
    def producer(self):
        return SingleItemProducer({})

    @classmethod
    def process_task(
        cls,
        cool_down: int = 60,
        break_period: int = 3600,
        headless: bool = False,
        **kwargs,
    ) -> None:
        cls(
            cool_down=cool_down,
            break_period=break_period,
            headless=headless,
            **kwargs,
        ).main()
