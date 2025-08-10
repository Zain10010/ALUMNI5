# Google Sheets integration temporarily disabled for deployment
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
import os.path
import pickle
from datetime import datetime
from models import Alumni, db

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of the spreadsheet.
SPREADSHEET_ID = '1P7v-jaxBcLzeaVmkdjXtu1iRgAHuyUPhD_TjNrZE_UI'
RANGE_NAME = 'Sheet1!A2:Z'  # Adjust range as needed

def get_google_sheets_service():
    # Temporarily disabled for deployment
    print("Google Sheets integration temporarily disabled")
    return None

def fetch_and_update_alumni():
    # Temporarily disabled for deployment
    print("Google Sheets integration temporarily disabled")
    return "Google Sheets integration temporarily disabled for deployment" 