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
from clear import clear

#pip3 install pandas
import pandas as pd #to covert the data to DataFrame

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
MAGENTA = fg("magenta")
R = attr("reset")


#Welcome screen banner
ascii_banner = BLUE + pyfiglet.figlet_format('Pulse Clinic', justify="center") + R

def clear_screen():
    """
    Function to clear the screen if no 
    """
    os.system('cls') #For Windows
    os.system('clear') #For Linux

def get_consultants():
    """
    Retrieve specialists that are available for booking
    """
    available_consultants = SHEET.worksheet("Availability").get_all_values()
    df =pd.DataFrame(available_consultants[1:],columns=available_consultants[0])
    doctor_names = list(df.columns[1:])
    for i, doctor_name in enumerate(doctor_names, start=1):
        print(f"{CYAN}{i}{R}  -  {doctor_name}\n")
    return df, doctor_names

def get_date(df, selected_doctor):
    """
    Function retrieves available months and days for selected doctor
    """
    df["Date"] = pd.to_datetime(df["Date"])
    filtered_df = df[df[selected_doctor].apply(lambda x: x.strip() != "")]
    unique_months = filtered_df["Date"].dt.month.unique()
    month_code_map = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    unique_days = filtered_df["Date"].dt.day.unique()
    month_codes = [month_code_map[month] for month in unique_months]
    
    # Return the month codes
    return month_codes, unique_days



def get_time(df, selected_doctor):
    """
    Function retrieves available time slots for selected doctor  
    """
    time_column = pd.to_datetime(df[selected_doctor], format='%H:%M', errors='coerce')


    valid_time_slots = time_column[time_column.notna()]

    # Extract unique time slots
    unique_time_slots = valid_time_slots.dt.time.unique()

    # Format time in HH:MM
    formatted_time_slots = [time.strftime('%H:%M') for time in unique_time_slots]

    return formatted_time_slots



def book_appointment():
    """
    Function provides instructions how to book an appointment.
    Provides Doctor/specialty options to select.
    Provides available dates to select.
    Provides available times to select.
    Confirms booking.
    Validates entries.
    """
    
    print(f"{BLUE}NEW APPOINTMENT BOOKING!\n")
    print("Please select required specialist from the options below:\n")
    df, doctor_names = get_consultants()
    

    while True:
        
        try:
            doctor_selection = int(input(f"\n\n{CYAN}Your selection: {R}\n\n"))
            if 1 <= doctor_selection <= len(doctor_names):
                selected_doctor = doctor_names[doctor_selection - 1]

                clear_screen()
                
                print(f"{MAGENTA}You selected {selected_doctor}{R}\n\n")
                month_codes, unique_days = get_date(df, selected_doctor)
                
                print("Please select month from the options below:\n")
                for i, month_code in enumerate(month_codes, start=1):
                    print(f"{CYAN}{i}{R} - {month_code}")

                while True:
                    try:
                        user_month_selection = int(input(f"\n\n{CYAN}Your selection: {R}\n\n"))
                        if 1 <= user_month_selection <= len(month_codes):
                            selected_month = month_codes[user_month_selection - 1]
                            formatted_time_slots = get_time(df, selected_doctor)
                            break
                        else:
                            print(f"{RED}Invalid selection!{R}\n")
                            print(f"{RED}Please select a valid month number{R}\n")
                    except ValueError:
                        print(f"{RED}Invalid selection!{R}\n")
                        print(f"{RED}Please enter a number{R}\n")
                break


                formatted_time_slots = get_time(df, selected_doctor)

                break
            else:
                print(f"{RED}Invalid selection!{R}\n")
                print(f"{RED}Please select a number{R}\n")
        except ValueError:
            menu_options()
            sleep(4)
            print(f"{RED}Invalid selection!{R}\n")
            print(f"{RED}Please select number 1 or 2{R}\n")

#def cancel_appointment():
   # """
   # Function provides instructions how to cancel existing appointment.
   # Confirms cancelation.
    #Validates entries.
   # """
   # print(f"{BLUE}CANCEL EXISTING BOOKING!\n")

def menu_options():
    """
    Function loads two options for the user to select and validates an input.
    """
    print(ascii_banner)
    print("Welcome to our patient portal!")
    print("Please select option 1 or 2 from the menu below:\n")
    print(f"{CYAN} 1 {R} - Book an Appointment")
    print(f"{CYAN} 2 {R} - Cancel existing Appointment\n")
    while True:
        user_selection = 0
        try:
            user_selection = (int(input(f"{CYAN}Your selection: {R}\n")))
            if user_selection == 1:
                clear_screen()
                book_appointment()
            elif user_selection == 2:
                clear_screen()
                #cancel_appointment()
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





 

def main_page():
    """
    Loads Welcome page for Pulse Clinic doctor booking system
    Provides selection to make a booking or cancel existing booking
    Validates entries
    """
    menu_options()
    
main_page()