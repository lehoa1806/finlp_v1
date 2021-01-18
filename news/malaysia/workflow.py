from typing import Dict

from machine import announcement2slack_post, news2slack_post
from machine.key_transform_stage import KeyTransformStage
from machine.postgres_batch_insert import PostgresBatchInsert
from news.scraper_job import ScraperJob
from news.scraper_task import ScraperTask
from news.utils.common import MY_TIMEZONE
from workflow.consumer import Consumer
from workflow.filter import Filter as FilteringStage
from workflow.hybrid_consumer import HybridConsumer
from workflow.pipeline import Pipeline


class Announcement2SlackPost(announcement2slack_post.Announcement2SlackPost):
    @property
    def channels(self) -> Dict:
        return self.setting.malaysia_channels


class News2SlackPost(news2slack_post.News2SlackPost):
    @property
    def channels(self) -> Dict:
        return self.setting.malaysia_channels


MALAYSIA_ANNOUNCEMENT_CONSUMER = HybridConsumer(
    consumers=[
        HybridConsumer(
            pipeline=Pipeline(
                stage=FilteringStage(
                    output_columns=[
                        'datetime',
                        'company',
                        'title',
                        'source',
                        'url',
                        'description',
                    ]
                )
            ),
            consumers=[
                PostgresBatchInsert(
                    table_name='malaysia_announcements',
                    batch_size=10,
                ),
            ],
        ),
        HybridConsumer(
            pipeline=Pipeline(
                stage=KeyTransformStage(
                    original_columns=[
                        'subscription',
                        'datetime',
                        'company',
                        'title',
                        'source',
                        'url',
                        'description',
                    ],
                    new_columns=[
                        'Subscription',
                        'Time',
                        'Company',
                        'Title',
                        'Source',
                        'Url',
                        'Description',
                    ]
                )
            ),
            consumers=[Announcement2SlackPost()],
        )
    ],
)


MALAYSIA_NEWS_CONSUMER = HybridConsumer(
    consumers=[
        HybridConsumer(
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
                    table_name='malaysia_articles',
                    batch_size=10,
                ),
            ],
        ),
        HybridConsumer(
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
    ],
)


class AnnouncementScraperJob(ScraperJob):
    @property
    def timezone(self) -> str:
        return MY_TIMEZONE

    @property
    def pipeline(self) -> Pipeline:
        raise NotImplementedError

    @property
    def consumer(self) -> Consumer:
        return MALAYSIA_ANNOUNCEMENT_CONSUMER


class AnnouncementScraperTask(ScraperTask):
    @property
    def pipeline(self) -> Pipeline:
        raise NotImplementedError

    @property
    def consumer(self) -> Consumer:
        return MALAYSIA_ANNOUNCEMENT_CONSUMER


class NewsScraperJob(ScraperJob):
    @property
    def timezone(self) -> str:
        return MY_TIMEZONE

    @property
    def pipeline(self) -> Pipeline:
        raise NotImplementedError

    @property
    def consumer(self) -> Consumer:
        return MALAYSIA_NEWS_CONSUMER


class NewsScraperTask(ScraperTask):
    @property
    def pipeline(self) -> Pipeline:
        raise NotImplementedError

    @property
    def consumer(self) -> Consumer:
        return MALAYSIA_NEWS_CONSUMER
