from argparse import Namespace

from common.argument_parser import ArgumentParser
from machine.key_transform_stage import KeyTransformStage
from machine.news2slack_post import News2SlackPost
from machine.postgres_batch_insert import PostgresBatchInsert
from news.utils.common import MY_TIMEZONE
from workflow.consumer import Consumer
from workflow.filter import Filter as FilteringStage
from workflow.hybrid_consumer import HybridConsumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer


class ScraperJob(Job):
    def __init__(self, table: str) -> None:
        super().__init__()
        self.table = table

    def parse_args(self) -> Namespace:
        parser = ArgumentParser(
            description='Script to scrape articles from Malaysia NewsPapers',
        )
        parser.add_date_input(
            'start-time',
            timezone=MY_TIMEZONE,
        )
        parser.add_date_input(
            'end-time',
            timezone=MY_TIMEZONE,
        )
        parser.add_argument(
            'headless', action='store_true',
            help='Run in headless mode',
        )

        return parser.arguments

    @property
    def consumer(self) -> Consumer:
        postgre = HybridConsumer(
            pipeline=Pipeline(
                stage=FilteringStage(
                    output_columns=[
                        'datetime',
                        'category',
                        'title',
                        'source',
                        'content',
                        'url',
                    ]
                )
            ),
            consumers=[
                PostgresBatchInsert(
                    table_name=self.table,
                    batch_size=10,
                ),
            ],
        )
        slack = HybridConsumer(
            pipeline=Pipeline(
                stage=KeyTransformStage(
                    original_columns=[
                        'subscription',
                        'datetime',
                        'category',
                        'title',
                        'source',
                        'content',
                        'url',
                    ],
                    new_columns=[
                        'Subscription',
                        'Time',
                        'Category',
                        'Title',
                        'Source',
                        'Content',
                        'Url',
                    ]
                )
            ),
            consumers=[News2SlackPost()],
        )
        return HybridConsumer(
            consumers=[postgre, slack]
        )

    @property
    def pipeline(self) -> Pipeline:
        raise NotImplementedError

    @property
    def producer(self):
        return SingleItemProducer({
            'start_time': self.args.start_time,
            'end_time': self.args.end_time,
        })
