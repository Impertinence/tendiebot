import pickle
import os.path
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None
if os.path.exists('sheets_token.json'):
    creds = Credentials.from_authorized_user_file('files/sheets_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'files/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('files/sheets_token.json', 'w') as token:
        token.write(creds.to_json())

service = build("sheets", "v4", credentials=creds)
sheets = service.spreadsheets()
    
class SHEETS():
    def __init__(self, spreadsheet_id, spreadsheet_name):
        self.SPREADSHEET_ID = spreadsheet_id
        self.SPREADSHEET_NAME = spreadsheet_name

    def getSheetsContent(self):
        results = sheets.values().get(spreadsheetId=self.SPREADSHEET_ID, range="Sheet1!A:A").execute()
        ticker_list = []

        for val in results['values']:
            if val[0] != "Tickers":
                ticker_list.append(val[0])

        return ticker_list
