from argparse import Namespace

from google_apis.auth import GoogleAuth
from google_apis.gmail import Gmail
from machine.google_email_sender import EmailSender
from machine.postgres_batch_delete import PostgresBatchDelete
from news.utils.common import MY_TIMEZONE
from utils.argument_parser import ArgumentParser
from workflow.filter import Filter
from workflow.hybrid_consumer import HybridConsumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer

from .article_querying_stage import ArticleQueryingStage


class Worker(Job):
    def parse_args(self) -> Namespace:
        parser = ArgumentParser(description='Script to send news to email')
        parser.add_date_input(
            "report-time",
            timezone=MY_TIMEZONE,
        )
        return parser.arguments

    @property
    def consumer(self) -> HybridConsumer:
        deleter = HybridConsumer(
            consumers=[
                PostgresBatchDelete(table_name='news_to_email_all',
                                    batch_size=10),
            ],
            pipeline=Pipeline(
                stage=Filter(output_columns=['news_id']),
            )
        )
        email_sender = EmailSender(
            gmail=Gmail(GoogleAuth()),
            report_time=self.args.report_time,
        )
        return HybridConsumer(
            consumers=[email_sender, deleter]
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
