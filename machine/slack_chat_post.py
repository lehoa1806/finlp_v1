from typing import Dict

from slackbot.slack_bot import SlackBot
from workflow.consumer import Consumer


class SlackChatPost(Consumer):
    def __init__(
        self,
    ) -> None:
        self.bot = SlackBot()

    def process(self, item: Dict) -> None:
        raise NotImplementedError
