#Import modules for working with Google Sheets
import gspread
from google.oauth2.service_account import Credentials #to handle authentication

#pip3 install pyfiglet
import pyfiglet

#pip3 install colored
from colored import fg, bg, attr

#importing module to clear screen
import os
from time import sleep

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

def clear_screen():
    """
    Function to clear the screen if no 
    """
    os.system('cls') #For Windows
    os.system('clear') #For Linux

def main_page():
    """
    Loads Welcome page for Pulse Clinic doctor booking system
    Provides selection to make a booking or cancel existing booking
    Validates entries
    """
    def menu_options():
        """
        Function loads 1 options for the user to select and validates an input.
        """
        print(ascii_banner)
        print("Welcome to our patient portal!")
        print("Please select option 1 or 2 from the menu below:\n")
        print(f"{CYAN} 1 {R} - Book an Appointment")
        print(f"{CYAN} 2 {R} - Cancel existing Appointment\n")

    menu_options()
    while True:
        user_selection = 0
        try:
            user_selection = (int(input(f"{CYAN}Your selection: {R}\n")))
            if user_selection == 1:
                clear_screen()
                book_appointment()
            elif user_selection == 2:
                clear_screen()
                cancel_appointment()
            else:
                clear_screen()
                menu_options()
                print(f"{RED}Invalid selection!{R}\n")
                print(f"{RED}Please select number 1 or 2{R}\n")
        except ValueError:
            clear_screen()
            menu_options()
            sleep(4)
            print(f"{RED}Invalid selection!{R}\n")
            print(f"{RED}Please select number 1 or 2{R}\n")
main_page()

        

