import datetime
import os.path
import calendar_building_blocks as cbb
import calendar_details as cd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from event_creator import get_and_print_events, create_event
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
    # creds = handle_authentication()
    # print("Now that we are authenticated, we can start calling the API:")
    # The 2 commented lines below make API calls to get event info and create all day events.
    # get_and_print_events(creds)
    # create_event(all_day_event, creds)

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
    print(period_block_names)
    print(blocks_of_the_day)
    for periods in time_schedule.items():
        print(periods)

    # Apply rotating day pattern to both semesters, then combine to make a year-long list.
    s1_rotation_days = cbb.apply_rotation_days(cd.semester_1, cd.rotation_day_names)
    s2_rotation_days = cbb.apply_rotation_days(cd.semester_2, cd.rotation_day_names)
    school_year_rotation_days = s1_rotation_days + s2_rotation_days

    # Add a column for RotationDays to the school_calendar_info dataframe.
    cd.df['RotationDays'] = school_year_rotation_days

    for i in range(cd.periods_per_day):
        cd.df[f'Period {i + 1}'] = cd.df['RotationDays']
        for j in range(len(cd.rotation_day_names)):
            cd.df.loc[cd.df['RotationDays'] == cd.rotation_day_names[j], f'Period {i + 1}'] = blocks_of_the_day[cd.rotation_day_names[j]][i]

    print(cd.df)
    print("Bye")


if __name__ == "__main__":
    main()
