from argparse import Namespace

from common.argument_parser import ArgumentParser
from machine.postgres_batch_delete import PostgresBatchDelete
from workflow.filter import Filter
from workflow.hybrid_consumer import HybridConsumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer

from .announcement2slack_post import Announcement2SlackPost
from .announcement_querying_stage import AnnouncementQueryingStage


class Worker(Job):
    def parse_args(self) -> Namespace:
        parser = ArgumentParser(
            description='Script to send announcements to slack')
        return parser.arguments

    @property
    def consumer(self) -> HybridConsumer:
        deleter = HybridConsumer(
            consumers=[
                PostgresBatchDelete(table_name='announcement_to_slack_all',
                                    batch_size=10),
            ],
            pipeline=Pipeline(
                stage=Filter(output_columns=['announcement_id']),
            )
        )
        return HybridConsumer(
            consumers=[Announcement2SlackPost(), deleter]
        )

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=AnnouncementQueryingStage()
        )

    @property
    def producer(self):
        return SingleItemProducer({})


if __name__ == "__main__":
    Worker().main()
