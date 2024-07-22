import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from progress.spinner import Spinner
from school_specific_info import test_ABCD_calendar_id, ABCD_calendar_id

current_calendar_id = ABCD_calendar_id

menu_options = ["(a) View names for each individual block in the schedule.",
                "(b) View all blocks that are assigned to each rotation day.",
                "(c) View the current time schedule for a full school day.",
                "(d) View the entire calendar dataframe.",
                "(e) Create all rotation day events on Google Calendar.",
                "(f) Get a list of upcoming events to work with from Google Calendar.",
                "(x) Exit program."
                ]

event_menu_options = ["(a) Nothing. Return to the main menu.",
                      "(b) Select events to delete.",
                      "(c) Delete all listed events",
                      ]


def welcome_message():
    print()
    print("Calendar Helper running.")
    print("What would you like to do? (Please choose from the list)")


def display_menu(menu):
    """Displays a menu to the user. Menu options will allow users to view data that is available to the program.
    Additionally, users can choose options that will initiate event creation on a Google Calendar."""
    # print()
    # print("Calendar Helper running.")
    # print("What would you like to do? (Please choose from the list)")
    for option in menu:
        print("    " + option)


def double_check_user_choice(dataframe, calendar_id):
    """Currently this function is tailored to one other event_creator function. This should be adjusted to allow
    for all calls to Google Calendar API to be double-checked before running. This way the user will be able to see
    how many events will be created, and which calendar or calendars they will be created on."""
    print("Are you sure you wish to proceed?")
    print(f"Please note: proceeding will create {dataframe.shape[0]} events.")
    print(f"The events will be created on the Google Calendar with the following calendarId:")
    print(f"{calendar_id}")
    proceed_or_not = input("Will you continue? (y/n): ")
    return proceed_or_not


def get_and_print_events(creds, calendar_id, number_of_events=10):
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print(f"Getting the upcoming {number_of_events} events")
        events_result = (service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=number_of_events,
            singleEvents=True,
            orderBy="startTime",
        )
                         .execute()
                         )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_id = event["id"]
            print(f"    ({events.index(event)}) "
                  f"Summary: {event['summary']} "
                  f"| Start: {start} "
                  f"| Event_Id: {event_id}")

        return events

    except HttpError as error:
        print(f"An error occurred: {error}")


def work_with_events(creds, calendar_id, number_of_events, events_to_work_with):
    still_working_with_events = True

    while still_working_with_events:
        print()
        print(f"What would you like to do with the {number_of_events} events listed above?")
        display_menu(event_menu_options)
        user_input = input(">>> ")
        if user_input.lower() == "a":
            still_working_with_events = False
            print("Returning to main menu.")
        elif user_input.lower() == "b":
            delete_events(creds, calendar_id, events_to_work_with)
            still_working_with_events = False
        elif user_input.lower() == "c":
            delete_events_in_bulk(creds, calendar_id, events_to_work_with)
            still_working_with_events = False


def create_event(event, creds):
    service = build("calendar", "v3", credentials=creds)
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def create_rotation_day_events(event, creds, start_date, end_date, summary, calendar_id):
    # Set the current date and summary name for the event based on the row in the dataframe.
    event["start"]["date"] = str(start_date)[:10]
    event["end"]["date"] = str(end_date)[:10]
    event["summary"] = f"{summary} Day"
    print(event["start"]["date"], event["summary"])

    # Calling the Google Calendar API here.
    service = build("calendar", "v3", credentials=creds)
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def delete_events(creds, calendar_id, events_to_work_with):
    # try:
    selecting_events_to_delete = True

    while selecting_events_to_delete:
        print("Each listed event is associated with a number in parenthesis.")
        print("Enter the number for each event you would like to delete, separated by commas (don't use spaces).")
        print("Alternatively, enter a range of events to delete, separated by \"-\" (i.e. 7-22).")
        print("The example range would delete events 7 through 22, leaving events 1-6 and 23-n on the calendar.")
        selected_events = input(">>> ")
        if "-" in selected_events:
            slice_values = selected_events.split("-")
            try:
                slice_values = [int(num[0:]) for num in slice_values]
                print(slice_values)
                events_to_delete = list(range(slice_values[0], slice_values[1] + 1))
                print(events_to_delete)
                selecting_events_to_delete = False
            except ValueError:
                events_to_delete = []
                print("Please enter a valid range of events to delete.")
        else:
            events_to_delete = selected_events.split(",")
            try:
                events_to_delete = [int(num[0:]) for num in events_to_delete]
                selecting_events_to_delete = False
            except ValueError:
                events_to_delete = []
                print("Please enter a valid list of events to delete.")

        if not events_to_delete:
            print("No events to delete.")
        else:
            print("The following events will be deleted")
            for event_number in events_to_delete:
                print(f"    Event id number: {events_to_work_with[event_number]['id']} "
                      f"| Name: {events_to_work_with[event_number]['summary']} "
                      f"| Date: {events_to_work_with[event_number]['start']}")
            confirmation = input("Would you like to proceed? (y/n): ")
            confirm_delete(creds, calendar_id, events_to_work_with, events_to_delete, confirmation)


def delete_events_in_bulk(creds, calendar_id, events_to_work_with):
    # try:
    events_to_delete = list(range(0, len(events_to_work_with)))
    print(f"Are you sure you want to delete all {len(events_to_work_with)} events that were listed earlier? (y/n): ")
    confirmation = input(">>> ")
    confirm_delete(creds, calendar_id, events_to_work_with, events_to_delete, confirmation)


def confirm_delete(creds, calendar_id, events_to_work_with, events_to_delete, confirmation):
    if confirmation.lower() == "y":
        try:
            service = build("calendar", "v3", credentials=creds)
            with Spinner('Deleting... ') as bar:
                for event_number in events_to_delete:
                    service.events().delete(calendarId=calendar_id, eventId=events_to_work_with[event_number]['id']).execute()
                    bar.next()
            print("Events deleted. Returning to main menu.")
        except HttpError as error:
            print(f"An error occurred: {error}")
    else:
        print("Cancelling deletion and returning to main menu.")
