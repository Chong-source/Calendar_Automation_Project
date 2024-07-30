import calendar_building_blocks as cbb
import calendar_details as cd
from calendar_details import period_block_names, blocks_of_the_day, time_schedule
from event_templates import all_day_event, timed_event
from main_functions import (
    get_and_print_events, create_rotation_day_events, create_teacher_class_event, current_calendar_id, welcome_message,
    display_menu, menu_options, double_check_user_choice, work_with_events, handle_authentication
)


def main():
    run_program = True
    creds = handle_authentication()

    while run_program:
        welcome_message()
        display_menu(menu_options)
        user_input = input(">>> ")
        if user_input.lower() == "a":
            print(period_block_names)
        elif user_input.lower() == "b":
            for day in blocks_of_the_day:
                print(f"{day} day has blocks: {blocks_of_the_day[day]}")
            print(blocks_of_the_day)
        elif user_input.lower() == "c":
            for periods, times in time_schedule.items():
                print(periods, times)
            print(time_schedule["Period 1"][0].time())
        elif user_input.lower() == "d":
            print(cd.df)
            print(cd.exploded)
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
            # The next 3 lines regarding Pandas options assist with display in the terminal only.
            cd.pd.options.display.max_columns = None
            cd.pd.options.display.max_rows = None
            cd.pd.set_option('display.width', 400)

            print(cd.merged.head(10))
            print(cd.merged.shape)

            # All events in the dataframe can be created on Google Calendar if the following code runs.
            action = input("What would you like to do with these events? (p)ush to Google Calendar / (g)o back: ")
            if action.lower() == "p":
                event_creation_count = 0
                for period in cd.merged.itertuples(index=False):
                    create_teacher_class_event(timed_event, creds, period[0], period[4], period[5], period[7], period[3], period[10])
                    event_creation_count += 1
                    print(f"Event number: {event_creation_count}")
                print(f"Total number of events created: {event_creation_count}")
        elif user_input.lower() == "i":
            print(cd.merged.at[0, "School Days"])
            print(type(cd.merged.at[0, "School Days"]))
            print(cd.merged.at[0, "School Days"].day_name())
            print(cd.merged.at[0, "School Days"].day_name() == "Tuesday")
            print(cd.merged.at[1, "School Days"].day_name() == "Tuesday")
            tuesday_df = cd.merged.loc[cd.merged["School Days"].day_name() == "Tuesday"]
            print(tuesday_df)
        elif user_input.lower() == "j":
            chosen_calendar = input("Which teacher's calendar would you like to view (enter their calendar id): ")
            single_teacher = cd.merged[cd.merged.CalendarID == chosen_calendar].reset_index(drop=True)
            # The next 3 lines regarding Pandas options assist with display in the terminal only.
            cd.pd.options.display.max_columns = None
            cd.pd.options.display.max_rows = None
            cd.pd.set_option('display.width', 400)
            single_teacher = single_teacher[:10]
            print(single_teacher[:10])
            action = input("What would you like to do with these events? (p)ush to Google Calendar / (g)o back: ")
            if action.lower() == "p":
                event_creation_count = 0
                for period in single_teacher.itertuples(index=False):
                    create_teacher_class_event(timed_event, creds, period[0], period[4], period[5], period[7], period[3], period[10])
                    event_creation_count += 1
                    print(f"Event number: {event_creation_count}")
                print(f"Total number of events created: {event_creation_count}")
        elif user_input.lower() == "x":
            run_program = False
            break
        else:
            print("Invalid input. Please try again.")

        # By prompting the user for input, the program allows the current output to stay in the main focus before
        # jumping to the main menu again.
        continue_key = input("\nPress any key to continue: ")

    print("Exiting Program")


if __name__ == "__main__":
    main()