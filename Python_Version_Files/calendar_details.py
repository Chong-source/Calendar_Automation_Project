import pandas as pd
import numpy as np
import calendar_building_blocks as cbb

from datetime import date, time, datetime, timedelta
from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay


# Information needed to create period block names
days_per_rotation = 4  # int(input("How many days are in each rotation?: "))
periods_per_day = 6  # int(input("How many periods are in each day?: "))
periods_per_rotation = 24  # int(input("How many periods are in each rotation?: "))
classes_to_schedule = 8  # int(input("How many classes must fit in the rotation schedule?: "))
letters_for_period_names = "abcdefghijklmnopqrstuvwxyz"
rotation_day_names = "ABCD"

# Information needed to create daily schedule.
# Arithmetic is not possible with times only. Need to recheck this.
start_of_period = datetime(year=2024, month=7, day=1, hour=7, minute=45)
end_of_school_day = datetime(year=2024, month=7, day=1, hour=14, minute=35)
length_of_period = timedelta(minutes=+55)  # was 55 for normal / 50 for tuesdays
travel_time = timedelta(minutes=+5)
number_of_breaks = 1  # Not including lunch
break_after_x_periods = 2
length_of_break = timedelta(minutes=15)  # was 15 for normal / 45 for tuesdays
lunch_after_x_periods = 4
length_of_lunch = timedelta(minutes=35)

# Bookend dates for the school year (use YYYY-MM-DD format)
# As I don't yet know how to skip multiple weeks via a custom holiday calendar, it is much easier to
# split the school year into quarters (even though the year runs on semesters) and build those quarters
# around the beginnings and endings of long holidays.

quarter1_start_date = '2024-08-05'  # First day of the school year.
quarter1_end_date = '2024-10-11'  # October break starts after this day.
quarter2_start_date = '2024-10-21'  # School back in session this day after October break.
quarter2_end_date = '2024-12-13'  # December break starts after this day.
quarter3_start_date = '2025-01-07'  # First day of the second semester.
quarter3_end_date = '2025-04-04'  # April break starts after this day.
quarter4_start_date = '2025-04-21'  # School back in session this day after April break.
quarter4_end_date = '2025-06-06'  # Last day of the school year.


class SchoolHolidayCalendar(AbstractHolidayCalendar):
    """A class to hold all custom holidays for the school year."""
    rules = [
        Holiday('Mother\'s Day', month=8, day=12),
        Holiday('Conference Day', month=10, day=4),
        Holiday('PSAT Testing', month=10, day=11),  # School in session, but no assigned letter day.
        Holiday('Chulalongkorn Day', month=10, day=23),
        Holiday('Father\'s Day', month=12, day=5),
        Holiday('Last Day of Semester 1', month=12, day=13),  # School in session, but no assigned letter day.
        Holiday('Wai Kru', month=1, day=17),
        Holiday('Makha Bucha Day', month=2, day=12),
        Holiday('Conference Day', month=2, day=28),
        Holiday('CMCIS PD Day', month=3, day=7),
        Holiday('Thai Labor Day', month=5, day=1),
        Holiday('Coronation Day', month=5, day=5),
        Holiday('Visakha Bucha Day', month=5, day=12),
        Holiday('Queen Suthida\'s Birthday', month=6, day=3),
        Holiday('Last Day of School', month=6, day=6),  # School in session, but no assigned letter day.
    ]


# Create a custom Business Day calendar that includes school holidays.
calendar_minus_school_holidays = CustomBusinessDay(calendar=SchoolHolidayCalendar())

# Create datetimeindexes for each quarter.
s1_quarter1 = pd.date_range(quarter1_start_date, quarter1_end_date, freq=calendar_minus_school_holidays)
s1_quarter2 = pd.date_range(quarter2_start_date, quarter2_end_date, freq=calendar_minus_school_holidays)
s2_quarter3 = pd.date_range(quarter3_start_date, quarter3_end_date, freq=calendar_minus_school_holidays)
s2_quarter4 = pd.date_range(quarter4_start_date, quarter4_end_date, freq=calendar_minus_school_holidays)

# Create datetimeindexes for each semester and then combine them for the full year.
# To check for mismatches in size --> print(semester_1.size, semester_2.size, school_year_calendar.size)
# Temporarily removing semester 2 so that only semester 1 dates can be used.
semester_1 = s1_quarter1.union(s1_quarter2)
# semester_2 = s2_quarter3.union(s2_quarter4)
school_days_in_session = semester_1  #.union(semester_2)

# Create base of dataframe containing dates for all school days.
df = pd.DataFrame(school_days_in_session, columns=['SchoolDays'])

# Create a dataframe containing all of the teachers' schedules.
schedules = pd.read_csv('teacher_schedules.csv', index_col=0)

# Create the names for each individual block that is in the schedule.
period_block_names = cbb.create_period_block_names(letters_for_period_names,
                                                   periods_per_rotation,
                                                   classes_to_schedule)

# Assign each rotation day a set of blocks equal to the number of periods per day.
blocks_of_the_day = cbb.assign_block_names_to_periods(periods_per_day,
                                                      rotation_day_names,
                                                      period_block_names)

# Create the timetable that holds start and end information for all events in a school day.
time_schedule = cbb.create_period_times(periods_per_day, start_of_period,
                                        length_of_period, travel_time,
                                        break_after_x_periods, length_of_break,
                                        lunch_after_x_periods, length_of_lunch,
                                        end_of_school_day)

# Apply rotating day pattern to both semesters, then combine to make a year-long list.
# Temporarily changing it to only be dates for the 1st semester of school.
s1_rotation_days = cbb.apply_rotation_days(semester_1, rotation_day_names)
# s2_rotation_days = cbb.apply_rotation_days(semester_2, rotation_day_names)
school_year_rotation_days = s1_rotation_days  # + s2_rotation_days

# Add a column for RotationDays to the school_calendar_info dataframe.
df['RotationDays'] = school_year_rotation_days

# Add a new column for each period. Values in the columns will show which sub blocks are in the period for
# each specific rotation day.
# for i in range(cd.periods_per_day):
#     cd.df[f'Period {i + 1}'] = cd.df['RotationDays']
#     for j in range(len(cd.rotation_day_names)):
#         cd.df.loc[cd.df['RotationDays'] == cd.rotation_day_names[j],
#         f'Period {i + 1}'] = blocks_of_the_day[cd.rotation_day_names[j]][i]

# Changing the commented section above to add just one column of all sub blocks (as a list joined to a string)
df['Periods'] = df['RotationDays']
df['Periods'] = df['Periods'].astype('object')
for i in range(len(rotation_day_names)):
    df.loc[df['RotationDays'] == rotation_day_names[i], 'Periods'] = blocks_of_the_day[
        rotation_day_names[i]]

# Surely there is a better way, but now that string of sub blocks is being changed back into a list.
# Once it is a list it can be exploded.
df['Periods'] = df['Periods'].str[0:].str.split(',').tolist()

# This exploded dataframe has each period for each day on in a separate row now.
exploded = df.explode('Periods', ignore_index=False)
# Merge the exploded dataframe with teacher schedules. This results in a dataframe that has every single
# class period for all teachers on in a separate row. Almost ready to be sent to Google Calendar.
merged = exploded.merge(schedules, how='inner', on='Periods')
# To avoid the next line, ensure that the teacher schedule CSV only has one semester.
# merged = merged[merged.Term != 'S2']
# Sort by teacher, then day. When pushing to Google Calendar this will allow events to be created for one
# teacher before moving on to the next.
merged = merged.sort_values(['Teacher Name', 'SchoolDays']).reset_index(drop=True)

# Create new columns: one for weekday names, one for Startimes, one for Endtimes
weekdays = merged.SchoolDays.dt.day_name()
merged.insert(loc=1, column='WeekDay', value=weekdays)
merged.insert(loc=4, column='StartTime', value=merged['Periods'])
merged.insert(loc=5, column='EndTime', value=merged['Periods'])


# Assign each rotation day a set of blocks equal to the number of periods per day, this time in list format.
list_blocks_of_the_day = cbb.assign_block_names_to_periods(periods_per_day, rotation_day_names, period_block_names,
                                                           False)

# Assign each period a set of blocks that can happen during that period.
periods_of_the_rotation = cbb.identify_all_periods_n(periods_per_day, list_blocks_of_the_day)
# print(list_blocks_of_the_day)
# print(periods_of_the_rotation)

# Set the start and end times for all periods on all days except Tuesdays.
# Tuesdays are skipped because this unique school schedule alters the period times every Tuesday.
cbb.set_start_times(merged, periods_of_the_rotation, time_schedule)
cbb.set_end_times(merged, periods_of_the_rotation, time_schedule)

# Make time changes necessary for Tuesday schedule.
length_of_period = timedelta(minutes=+50)  # was 55 for normal / 50 for tuesdays
length_of_break = timedelta(minutes=45)  # was 15 for normal / 45 for tuesdays

# Create the Tuesday timetable that holds start and end information for all events in a school day.
tuesday_time_schedule = cbb.create_period_times(periods_per_day, start_of_period,
                                                length_of_period, travel_time,
                                                break_after_x_periods, length_of_break,
                                                lunch_after_x_periods, length_of_lunch,
                                                end_of_school_day)

# Now set all the start and end times for all periods on all Tuesdays.
cbb.set_tuesday_start_times(merged, periods_of_the_rotation, tuesday_time_schedule)
cbb.set_tuesday_end_times(merged, periods_of_the_rotation, tuesday_time_schedule)
