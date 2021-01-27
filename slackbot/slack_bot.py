import logging
import time
from typing import Dict, Iterator, Tuple
from urllib.error import URLError

from slack.web.client import WebClient
from slack.web.slack_response import SlackResponse

from .slack_message import SlackMessage


class SlackBot:
    MAX_RETRY = 5
    RETRY_INTERVAL = 0.5

    def __init__(
        self,
        token: str,
    ) -> None:
        self.client = WebClient(token=token)
        self.channels: Dict[str, str] = dict(self.get_channels())

    def get_channels(
        self,
    ) -> Iterator[Tuple[str, str]]:
        response = self.client.conversations_list()
        for channel in response['channels']:
            if channel['is_channel']:
                yield channel['name'], channel['id']

    def get_users(
        self,
    ) -> Iterator[Tuple[str, str]]:
        response = self.client.users_list()
        for user in response['members']:
            yield user['name'], user

    def chat_post(
        self,
        channel: str,
        message: SlackMessage,
    ) -> SlackResponse:
        message = message.to_message()
        retry = 0
        while True:
            try:
                retry += 1
                return self.client.chat_postMessage(
                    channel=self.channels[channel],
                    **message.to_dict(),
                )
            except URLError as err:
                if retry <= self.MAX_RETRY:
                    logging.error(
                        f'Failed to send data (error={err}). Retrying...')
                else:
                    logging.warning(
                        f'Failed to send data (error={err}). Stopped...')
                    break
            time.sleep(self.RETRY_INTERVAL)
