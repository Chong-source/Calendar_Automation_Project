import datetime
import os.path
import calendar_building_blocks as cbb
import calendar_details as cd
import main_functions as mf
import string

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from main_functions import get_and_print_events, create_event, create_rotation_day_events, current_calendar_id
from event_templates import all_day_event

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def handle_authentication():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("../Credentials/token.json"):
        creds = Credentials.from_authorized_user_file("../Credentials/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "../Credentials/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("../Credentials/token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def main():
    run_program = True
    creds = handle_authentication()

    # Create the names for each individual block that is in the schedule.
    period_block_names = cbb.create_period_block_names(cd.letters_for_period_names,
                                                       cd.periods_per_rotation,
                                                       cd.classes_to_schedule)

    # Assign each rotation day a set of blocks equal to the number of periods per day.
    blocks_of_the_day = cbb.assign_block_names_to_periods(cd.periods_per_day,
                                                          cd.rotation_day_names,
                                                          period_block_names)

    # Create the timetable that holds start and end information for all events in a school day.
    time_schedule = cbb.create_period_times(cd.periods_per_day, cd.start_of_period,
                                            cd.length_of_period, cd.travel_time,
                                            cd.break_after_x_periods, cd.length_of_break,
                                            cd.lunch_after_x_periods, cd.length_of_lunch,
                                            cd.end_of_school_day)

    # Apply rotating day pattern to both semesters, then combine to make a year-long list.
    s1_rotation_days = cbb.apply_rotation_days(cd.semester_1, cd.rotation_day_names)
    s2_rotation_days = cbb.apply_rotation_days(cd.semester_2, cd.rotation_day_names)
    school_year_rotation_days = s1_rotation_days + s2_rotation_days

    # Add a column for RotationDays to the school_calendar_info dataframe.
    cd.df['RotationDays'] = school_year_rotation_days

    # Add a new column for each period. Values in the columns will show which sub blocks are in the period for
    # each specific rotation day.
    for i in range(cd.periods_per_day):
        cd.df[f'Period {i + 1}'] = cd.df['RotationDays']
        for j in range(len(cd.rotation_day_names)):
            cd.df.loc[cd.df['RotationDays'] == cd.rotation_day_names[j],
            f'Period {i + 1}'] = blocks_of_the_day[cd.rotation_day_names[j]][i]

    while run_program:
        mf.welcome_message()
        mf.display_menu(mf.menu_options)
        user_input = input(">>> ")
        if user_input.lower() == "a":
            print(period_block_names)
        elif user_input.lower() == "b":
            for day in blocks_of_the_day:
                print(f"{day} day has blocks: {blocks_of_the_day[day]}")
        elif user_input.lower() == "c":
            for periods in time_schedule.items():
                print(periods)
        elif user_input.lower() == "d":
            print(cd.df)
        elif user_input.lower() == "e":
            decision = mf.double_check_user_choice(cd.df, current_calendar_id)
            if decision.lower() == "y":
                for row in cd.df.itertuples(index=False):
                    create_rotation_day_events(all_day_event, creds, row[0], row[0], row[1], current_calendar_id)
            else:
                print("Cancelling your choice and returning to main menu.")
        elif user_input.lower() == "f":
            try:
                number_of_events = int(input("How many events would you like to get? "))
                events = get_and_print_events(creds, current_calendar_id, number_of_events)
                mf.work_with_events(creds, events, number_of_events, current_calendar_id)
            except ValueError:
                print("Please enter an integer next time.")
        elif user_input.lower() == "x":
            run_program = False
        else:
            print("Invalid input. Please try again.")

    print("Exiting Program")


if __name__ == "__main__":
    main()