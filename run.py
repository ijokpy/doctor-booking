#Import modules for working with Google Sheets
import gspread
from google.oauth2.service_account import Credentials #to handle authentication

#pip3 install pyfiglet
import pyfiglet

#pip3 install colored
from colored import fg, bg, attr

#Define list of scopes that defines the access levels app requires
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

#Constant variables
#Load the service account credentials from the 'creds.json' file
CREDS = Credentials.from_service_account_file('creds.json')
#Using 'with_scopes' method to add specified OAuth 2.0 scopes to the credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
#Using 'gspread.authorize' method creating a client to interact with Google Sheets
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
#Opening google sheet
SHEET = GSPREAD_CLIENT.open('doctor_booking')

#Colours
RED = fg("red")
BLUE = fg("light_blue")
CYAN = fg("light_cyan")
R = attr("reset")


#Welcome screen banner
ascii_banner = BLUE + pyfiglet.figlet_format('Pulse Clinic', justify="center") + R



#def main_page():
   # """
    #Loads Welcome page for Pulse Clinic doctor booking system
   # Provides selection to make a booking or cancel existing booking
   # Validates entries
    #"""
