from datetime import datetime
from typing import Dict

from google_apis.gmail import Gmail
from utils.configs.setting import Setting
from workflow.consumer import Consumer

MESSAGE_TEMPLATE = '''<br /><b>{count}</b>.
<br />Time: {time}
<br />Title: <b>{title}</b>
<br />Category: <a style="color:#555"><b>{category}</b></a>
<br />Source: <a style="color:#555"><b>{source}</b></a>
<br />Url: <a rel="nofollow" style="text-decoration:none; color:#000">{url}</a>
<br />
'''


class EmailSender(Consumer):
    def __init__(
        self,
        gmail: Gmail,
        report_time: datetime,
    ) -> None:
        self.setting = Setting()
        self.gmail = gmail
        self.report_time = report_time.strftime('%b %d, %H:%M')

        self.message = 'New articles to <b>{}</b>:<br />'.format(
            self.report_time)
        self.count = 0

    def process(self, item: Dict) -> None:
        """
        Write item to message.
        :param item: Dict
        """
        time = item.get('Time')
        title = item.get('Title')
        category = item.get('Category')
        source = item.get('Source')
        url = item.get('Url')
        if any([time, category, title, source, url]):
            self.count += 1
            self.message = self.message + MESSAGE_TEMPLATE.format(
                count=self.count,  time=time, category=category,
                title=title, source=source, url=url,
            )

    def teardown(self, item: Dict) -> None:
        """
        Send email
        :param item: Stop()
        """
        if self.count > 1:
            message = self.gmail.create_message(
                sender=self.setting.email_sender,
                to=self.setting.email_receiver,
                subject='Market News: {}'.format(self.report_time),
                message_text=self.message,
            )
            self.gmail.send_message(message=message)
