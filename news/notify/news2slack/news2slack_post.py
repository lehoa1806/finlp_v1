from typing import Dict

from slack.web.classes.blocks import SectionBlock
from slack.web.classes.objects import TextObject

from machine.slack_chat_post import SlackChatPost
from slackbot.slack_message import SlackMessage


class News2SlackPost(SlackChatPost):
    def process(self, item: Dict) -> None:
        """
        Post messages to Slack channel.
        :param item: Dict
        """
        channel = item.get('Channel')
        time = item.get('Time')
        title = item.get('Title')
        category = item.get('Category')
        source = item.get('Source')
        url = item.get('Url')
        message = SlackMessage(
            title='{}: {}'.format(source.split('.')[0], title),
        ).add_context(
            elements=[TextObject(text=':calendar: {}'.format(time),
                                 subtype='mrkdwn')],
        ).add_section(
            section=SectionBlock(
                fields=['Category:\n*{}*'.format(category or 'N/A'),
                        'Source:\n*{}*'.format(source)],
            ),
        ).add_section(
            text=':newspaper: *{}*'.format(title or 'N/A'),
        ).add_context(
            elements=[TextObject(text=url, subtype='mrkdwn')],
        ).add_divider()
        self.bot.chat_post(
            channel=channel,
            message=message,
        )
