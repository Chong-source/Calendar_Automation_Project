menu_options = ["(a) View names for each individual block in the schedule.",
                "(b) View all blocks that are assigned to each rotation day.",
                "(c) View the current time schedule for a full school day.",
                "(d) View the entire calendar dataframe.",
                "(e) Create all rotation day events on Google Calendar.",
                "(x) Exit program."
                ]


def display_menu(menu_options):
    """Displays a menu to the user. Menu options will allow users to view data that is available to the program.
    Additionally, users can choose options that will initiate event creation on a Google Calendar."""
    print()
    print("Calendar Helper running.")
    print("What would you like to do? (Please choose from the list)")
    for option in menu_options:
        print("    " + option)


def double_check_user_choice(dataframe, current_calendar_id):
    """Currently this function is tailored to one other event_creator function. This should be adjusted to allow
    for all calls to Google Calendar API to be double-checked before running. This way the user will be able to see
    how many events will be created, and which calendar or calendars they will be created on."""
    print("Are you sure you wish to proceed?")
    print(f"Please note: proceeding will create {dataframe.shape[0]} events.")
    print(f"The events will be created on the Google Calendar with the following calendarId:")
    print(f"{current_calendar_id}")
    proceed_or_not = input("Will you continue? (y/n): ")
    return proceed_or_not
