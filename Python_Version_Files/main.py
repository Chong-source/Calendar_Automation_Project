import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import calendar_building_blocks as cbb
import calendar_details as cd
from event_templates import all_day_event
from main_functions import (
    get_and_print_events, create_rotation_day_events, current_calendar_id, welcome_message,
    display_menu, menu_options, double_check_user_choice, work_with_events
)

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
    # for i in range(cd.periods_per_day):
    #     cd.df[f'Period {i + 1}'] = cd.df['RotationDays']
    #     for j in range(len(cd.rotation_day_names)):
    #         cd.df.loc[cd.df['RotationDays'] == cd.rotation_day_names[j],
    #         f'Period {i + 1}'] = blocks_of_the_day[cd.rotation_day_names[j]][i]

    # Changing the commented section above to add just one column of all sub blocks (as a list joined to a string)
    cd.df['Periods'] = cd.df['RotationDays']
    cd.df['Periods'] = cd.df['Periods'].astype('object')
    for i in range(len(cd.rotation_day_names)):
        cd.df.loc[cd.df['RotationDays'] == cd.rotation_day_names[i], 'Periods'] = blocks_of_the_day[cd.rotation_day_names[i]]

    # Surely there is a better way, but now that string of sub blocks is being changed back into a list.
    # Once it is a list it can be exploded.
    cd.df['Periods'] = cd.df['Periods'].str[0:].str.split(',').tolist()

    exploded = cd.df.explode('Periods', ignore_index=False)

    while run_program:
        welcome_message()
        display_menu(menu_options)
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
            print(exploded)
        elif user_input.lower() == "e":
            decision = double_check_user_choice(cd.df, current_calendar_id)
            if decision.lower() == "y":
                for row in cd.df.itertuples(index=False):
                    create_rotation_day_events(all_day_event, creds, row[0], row[0], row[1], current_calendar_id)
            else:
                print("Cancelling your choice and returning to main menu.")
        elif user_input.lower() == "f":
            try:
                number_of_events = int(input("How many events would you like to get? "))
                events_to_work_with = get_and_print_events(creds, current_calendar_id, number_of_events)
                if not events_to_work_with:
                    print("There are no events to work with. Returning to main menu.")
                else:
                    work_with_events(creds, current_calendar_id, number_of_events, events_to_work_with)
            except ValueError:
                print("Please enter an integer next time.")
        elif user_input.lower() == "g":
            print(cd.schedules)
        elif user_input.lower() == "h":
            cd.pd.options.display.max_columns = None
            cd.pd.options.display.max_rows = None
            cd.pd.set_option('display.width', 400)
            merged = exploded.merge(cd.schedules, how='inner', on='Periods')
            merged = merged[merged.Term != 'S2']
            merged = merged.sort_values(['Teacher Name', 'School Days']).reset_index(drop=True)
            print(merged.head(40))
            print(merged.shape)
        elif user_input.lower() == "x":
            run_program = False
        else:
            print("Invalid input. Please try again.")

    print("Exiting Program")


if __name__ == "__main__":
    main()