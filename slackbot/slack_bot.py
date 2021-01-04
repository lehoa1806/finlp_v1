from typing import Dict, Iterator, Tuple

from slack.web.client import WebClient
from slack.web.slack_response import SlackResponse

from common.setting import Setting

from .slack_message import SlackMessage


class SlackBot:
    def __init__(
        self,
    ) -> None:
        self.client = WebClient(token=Setting().slack_token)
        self.channels: Dict[str, str] = dict(self.get_channels())

    def get_channels(
        self,
    ) -> Iterator[Tuple[str, str]]:
        response = self.client.channels_list()
        for channel in response['channels']:
            if channel['is_member']:
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
        response = self.client.chat_postMessage(
            channel=self.channels[channel],
            **message.to_dict(),
        )
        return response
