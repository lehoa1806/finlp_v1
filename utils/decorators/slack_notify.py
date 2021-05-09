import functools
import warnings

from slack.web.classes.objects import TextObject

from utils.dynamodb import Database
from slackbot.slack_bot import SlackBot
from slackbot.slack_message import SlackMessage
from utils.configs.setting import Setting


def slack_notify(func=None, *, func_type=None, func_name=None):
    """
    A decorator to send execution status to slack
    :param func: Function to be decorated
    :param func_type: Type of function to be decorated (task, job, function)
    :param func_name: A customized name of the function
    """
    if func is None:
        return functools.partial(
            slack_notify, func_type=func_type, func_name=func_name,
        )
    table = Database().get_tracking_table()
    slack_bot = SlackBot(Setting().devbot_token)

    @functools.wraps(func)
    def wrapper_alarm(*args, **kwargs):
        name = func_name or func.__qualname__
        track_info = table.get_item(
            partition_key=name,
            sort_key=func_type,
        ) or {
            'track_id': name,
            'track_type': func_type,
        } if func_type is not None else {}

        status = track_info.get('status', {})
        warnings.filterwarnings('ignore', '^(?!.*failed).*$')
        with warnings.catch_warnings(record=True) as warn:
            value = func(*args, **kwargs)
            if len(warn) <= 0 and status.get('last_status') == 'failed':
                message = SlackMessage(
                    title=f'Slack notification: {name}',
                ).add_header(
                    text=f':shamrock:   {name} is back to normal   :shamrock:',
                ).add_divider()
                slack_bot.chat_post(
                    channel='development',
                    message=message,
                )
                if track_info:
                    status.update({'last_status': 'passed'})
                    track_info.update({'status': status})
                    table.put_item(item=track_info)
            elif len(warn) > 0 and status.get('last_status') != 'failed':
                message = SlackMessage(
                    title=f'Slack notification: {name}',
                ).add_header(
                    text=f':bomb:   {name} failed   :bomb:',
                ).add_context(
                    elements=[TextObject(
                        text=f':pushpin: Description: \n*{warn[0].message}*',
                        subtype='mrkdwn',
                    )],
                ).add_divider()
                slack_bot.chat_post(
                    channel='development',
                    message=message,
                )
                if track_info:
                    status.update({'last_status': 'failed'})
                    track_info.update({'status': status})
                    table.put_item(item=track_info)
            elif len(warn) > 0 and status.get('last_status') == 'failed':
                message = SlackMessage(
                    title=f'Slack notification: {name}',
                ).add_header(
                    text=f':boom:   {name} failed again   :boom:',
                ).add_divider()
                slack_bot.chat_post(
                    channel='development',
                    message=message,
                )
        return value

    return wrapper_alarm
