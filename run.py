#Import modules for working with Google Sheets
import gspread
from google.oauth2.service_account import Credentials #to handle authentication

#Define list of scopes that defines the access levels app requires
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

#Load the service account credentials from the 'creds.json' file
CREDS = Credentials.from_service_account_file('creds.json')

#Using 'with_scopes' method to add specified OAuth 2.0 scopes to the credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

#Using 'gspread.authorize' method creating a client to interact with Google Sheets
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

#Opening google sheet
SHEET = GSPREAD_CLIENT.open('doctor_booking')

#Getting a worksheet from Google Sheet
availability = SHEET.worksheet('Availability')

#Retrieving all values from the 'Availability' worksheet to test API
data = availability.get_all_values()

print(data)