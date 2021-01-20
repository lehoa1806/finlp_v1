import functools
import logging
import random
import time
import warnings

from slack.web.classes.objects import TextObject

from aws_apis.dynamodb.database import Database as DynamoDB
from slackbot.slack_bot import SlackBot
from slackbot.slack_message import SlackMessage


def do_and_sleep(func=None, *, level: int = 0):
    """
    A decorator to perform a sleep after executing a function
    :param func: Function to be decorated
    :param level: int
    """
    if func is None:
        return functools.partial(do_and_sleep, level=level)

    @functools.wraps(func)
    def wrapper_do_and_sleep(*args, **kwargs):
        value = func(*args, **kwargs)
        sort_delay = random.randint(1, 9)
        long_delay = random.randint(2, 4) * level
        delay = 0.1 * sort_delay + long_delay
        logging.info('Sleep in {} seconds'.format(delay))
        time.sleep(delay)
        return value
    return wrapper_do_and_sleep


def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    """
    A decorator to print logs
    :param func: Function to be decorated
    :param level: Log level
    :param name: Logger name
    :param message: message
    """
    if func is None:
        return functools.partial(logged, level=level, name=name, message=message)
    logger = logging.getLogger(name)

    @functools.wraps(func)
    def wrapper_logged(*args, **kwargs):
        if level == logging.DEBUG and not message:
            logger.log(level, f'Leave: {func.__qualname__}')
        else:
            logger.log(level, message)
        value = func(*args, **kwargs)
        if level == logging.DEBUG and not message:
            logger.log(level, f'Leave: {func.__qualname__}')
        return value
    return wrapper_logged


def slack_notify(func=None, *, func_type=None):
    """
    A decorator to print logs
    :param func: Function to be decorated
    :param func_type: type of function to be decorated (task, job, function)
    """
    if func is None:
        return functools.partial(slack_notify, func_type=func_type)
    table = DynamoDB.load_database().get_tracking_table()
    slack_bot = SlackBot()

    @functools.wraps(func)
    def wrapper_alarm(*args, **kwargs):
        track_info = table.get_item(
            partition_key=func.__qualname__,
            sort_key=func_type,
        ) or {
            'track_id': func.__qualname__,
            'track_type': func_type,
        } if func_type is not None else {}

        status = track_info.get('status', {})
        warnings.filterwarnings('ignore', '^(?!.*failed).*$')
        with warnings.catch_warnings(record=True) as warn:
            value = func(*args, **kwargs)
            if len(warn) <= 0 and status.get('last_status') == 'failed':
                message = SlackMessage(
                    title=f'Slack notification: {func.__qualname__}',
                ).add_header(
                    text=f':shamrock:   {func.__qualname__} is back to normal   :shamrock:',
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
                    title=f'Slack notification: {func.__qualname__}',
                ).add_header(
                    text=f':bomb:   {func.__qualname__} failed   :bomb:',
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
                    title=f'Slack notification: {func.__qualname__}',
                ).add_header(
                    text=f':boom:   {func.__qualname__} failed again   :boom:',
                ).add_divider()
                slack_bot.chat_post(
                    channel='development',
                    message=message,
                )
        return value

    return wrapper_alarm