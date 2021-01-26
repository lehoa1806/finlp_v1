import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from utils.configs.setting import Setting

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.send',
]


class GoogleAuth:
    """
    Credentials wrapper for Google API.
    """
    def __init__(self) -> None:
        self.creds = None

    @property
    def credentials(self):
        """
        Initialize/load credentials.
        """
        # The file token.pickle stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        credentials_file = Setting().google_credentials_path
        token_file = Setting().google_token_path
        if not self.creds and os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                self.creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired \
                    and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES)
                self.creds = flow.run_local_server()
                # Save the credentials for the next run
                with open(token_file, 'wb') as token:
                    pickle.dump(self.creds, token)
        return self.creds
