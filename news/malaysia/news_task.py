from machine.key_transform_stage import KeyTransformStage
from machine.news2slack_post import News2SlackPost
from machine.postgres_batch_insert import PostgresBatchInsert
from workflow.consumer import Consumer
from workflow.filter import Filter as FilteringStage
from workflow.hybrid_consumer import HybridConsumer
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer
from workflow.task import Task

from .filter import Filter


class NewsTask(Task):
    def __init__(
        self,
        ft: Filter,
        table: str,
        start_time: str,
        end_time: str,
        headless: bool,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.filter = ft
        self.table = table
        self.start_time = start_time
        self.end_time = end_time
        self.headless = headless

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
            'start_time': self.start_time,
            'end_time': self.end_time,
        })

    @classmethod
    def process_task(
        cls,
        ft: Filter,
        table: str,
        start_time: str,
        end_time: str,
        **kwargs,
    ) -> None:
        cls(
            ft=ft, table=table,
            start_time=start_time, end_time=end_time,
            **kwargs,
        ).main()
