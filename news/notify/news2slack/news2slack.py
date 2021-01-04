from argparse import Namespace

from common.argument_parser import ArgumentParser
from machine.postgres_batch_delete import PostgresBatchDelete
from workflow.filter import Filter
from workflow.hybrid_consumer import HybridConsumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer

from .article_querying_stage import ArticleQueryingStage
from .news2slack_post import News2SlackPost


class Worker(Job):
    def parse_args(self) -> Namespace:
        parser = ArgumentParser(description='Script to send news to slack')
        return parser.arguments

    @property
    def consumer(self) -> HybridConsumer:
        deleter = HybridConsumer(
            consumers=[
                PostgresBatchDelete(table_name='news_to_slack_all',
                                    batch_size=10),
            ],
            pipeline=Pipeline(
                stage=Filter(output_columns=['news_id']),
            )
        )
        return HybridConsumer(
            consumers=[News2SlackPost(), deleter]
        )

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=ArticleQueryingStage()
        )

    @property
    def producer(self):
        return SingleItemProducer({})


if __name__ == "__main__":
    Worker().main()
