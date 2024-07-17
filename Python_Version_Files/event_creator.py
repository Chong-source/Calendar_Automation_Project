import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


current_calendar_id = 'c_523bfb7ac23003cd862371ef6efab433dd50f60f5cd1ed00fbd7d45530eff616@group.calendar.google.com'


def get_and_print_events(creds):
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
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
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


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

