import base64
import logging
import mimetypes
import os
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict

from googleapiclient.discovery import build

from google_apis.auth import GoogleAuth


class Gmail:
    """
    Gmail Api wrapper
    """
    def __init__(
        self,
        auth: GoogleAuth,
    ) -> None:
        self.auth = auth
        # Create authorized Gmail API service instance
        self.service = build('gmail', 'v1', credentials=self.auth.credentials)

    @classmethod
    def create_message(
        cls,
        sender: str,
        to: str,
        subject: str,
        message_text: str,
    ) -> Dict[str, str]:
        """
        Create a message for an email.

        :param sender: Email address of the sender
        :param to: Email address of the receiver
        :param subject: The subject of the email message
        :param message_text: The text of the email message
        :return: An object containing a base64url encoded email object
        """
        message = MIMEText(message_text, 'html')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {
            'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
        }

    @classmethod
    def create_message_with_attachment(
        cls,
        sender: str,
        to: str,
        subject: str,
        message_text: str,
        file: str,
    ) -> Dict[str, str]:
        """
        Create a message for an email.

        :param sender: Email address of the sender
        :param to: Email address of the receiver
        :param subject: The subject of the email message
        :param message_text: The text of the email message
        :param file: The path to the file to be attached
        :return: An object containing a base64url encoded email object
        """
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        with open(file, 'rb') as fp:
            if main_type == 'text':
                msg = MIMEText(fp.read(), _subtype=sub_type)  # type: ignore
            elif main_type == 'image':
                msg = MIMEImage(fp.read(), _subtype=sub_type)  # type: ignore
            elif main_type == 'audio':
                msg = MIMEAudio(fp.read(), _subtype=sub_type)  # type: ignore
            elif main_type == 'application':
                msg = MIMEApplication(fp.read(), _subtype=sub_type)  # type: ignore  # noqa
            else:
                msg = MIMEBase(main_type, sub_type)  # type: ignore
                msg.set_payload(fp.read())
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_message(
        self,
        message: Dict[str, Any],
        user_id: str = 'me',
    ) -> Dict[str, Any]:
        """
        Send an email message

        :param message: Message to be sent
        :param user_id: User's email address. The special value "me"
                        can be used to indicate the authenticated user
        :return: Sent Message
        """
        try:
            return self.service.users().messages().send(
                userId=user_id, body=message).execute()
        except Exception as error:
            logging.exception('An error occurred: %s' % error)
        return {}
