
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Permission to create and manage files created or opened
# by this application.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def authenticate_google_drive():

    creds = None

    # Check whether a previous authentication token exists.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json", SCOPES
        )

    # Refresh an expired token where possible.
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    # If there are no valid credentials, authenticate.
    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )

        creds = flow.run_local_server(port=0)

        # Save the authentication token for future use.
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Build the Google Drive API service.
    service = build("drive", "v3", credentials=creds)

    print("Google Drive authentication successful!")

    return service
