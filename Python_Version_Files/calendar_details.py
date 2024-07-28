import pandas as pd
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
length_of_period = timedelta(minutes=+55)
travel_time = timedelta(minutes=+5)
number_of_breaks = 1  # Not including lunch
break_after_x_periods = 2
length_of_break = timedelta(minutes=15)
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
semester_1 = s1_quarter1.union(s1_quarter2)
semester_2 = s2_quarter3.union(s2_quarter4)
school_days_in_session = semester_1.union(semester_2)

# Create base of dataframe containing dates for all school days.
df = pd.DataFrame(school_days_in_session, columns=['School Days'])

# Create a dataframe containing all of the teachers' schedules.
schedules = pd.read_csv('teacher_schedules.csv', index_col=0)
