import numpy as np


def create_period_times(periods_per_day, start_of_period, length_of_period, travel_time,
                        break_after_x_periods, length_of_break,
                        lunch_after_x_periods, length_of_lunch,
                        end_of_school_day):
    """Create a timetable that divides the day into periods based on information given
    in the calendar_details file. Returns a dictionary of the time_schedule."""
    time_schedule = {}
    period_number = 0

    for i in range(periods_per_day):
        if period_number < break_after_x_periods:
            time_schedule[f"Period {period_number + 1}"] = (start_of_period, start_of_period + length_of_period)
            start_of_period += (length_of_period + travel_time)
            period_number += 1
        elif period_number == break_after_x_periods:
            time_schedule[f"Break"] = (start_of_period - travel_time, start_of_period - travel_time + length_of_break)
            start_of_period += length_of_break
            time_schedule[f"Period {period_number + 1}"] = (start_of_period, start_of_period + length_of_period)
            start_of_period += (length_of_period + travel_time)
            period_number += 1
        elif (period_number > break_after_x_periods) and (period_number < lunch_after_x_periods):
            time_schedule[f"Period {period_number + 1}"] = (start_of_period, start_of_period + length_of_period)
            start_of_period += (length_of_period + travel_time)
            period_number += 1
        elif period_number == lunch_after_x_periods:
            time_schedule[f"Lunch"] = (start_of_period, start_of_period + length_of_lunch)
            start_of_period += length_of_lunch + travel_time
            time_schedule[f"Period {period_number + 1}"] = (start_of_period, start_of_period + length_of_period)
            start_of_period += (length_of_period + travel_time)
            period_number += 1
        elif (period_number > lunch_after_x_periods) and (start_of_period < end_of_school_day):
            time_schedule[f"Period {period_number + 1}"] = (start_of_period, start_of_period + length_of_period)
            start_of_period += (length_of_period + travel_time)
            period_number += 1

    return time_schedule


def create_period_block_names(letters_for_period_names, periods_per_rotation,
                              classes_to_schedule):
    """Takes a string of letters to use to create the period block names.
    Returns a list of period block names."""
    period_block_names = []
    number = 1
    for i in range(periods_per_rotation):
        period_letter_prefix = letters_for_period_names[i % classes_to_schedule]
        if not period_block_names:
            period_block_names.append(f"{period_letter_prefix}{number}")
        elif period_letter_prefix == letters_for_period_names[0]:
            number += 1
            period_block_names.append(f"{period_letter_prefix}{number}")
        else:
            period_block_names.append(f"{period_letter_prefix}{number}")
    return period_block_names


def apply_rotation_days(datetimeindex, rotation_day_names):
    """Takes a datetimeindex and applies a rotation day label for each day
    in the datetimeindex and adds it to a list. Returns a list the length of the datetimeindex."""
    rotating_pattern = []

    while len(rotating_pattern) < datetimeindex.size:
        for letter in rotation_day_names:
            if len(rotating_pattern) >= datetimeindex.size:
                break
            else:
                rotating_pattern.append(letter)
    return rotating_pattern


# def apply_periods_to_days(dataframe, blocks_of_the_day):
#     dataframe = dataframe.assign("Period 1" = dataframe[])


def assign_block_names_to_periods(periods_per_day, rotation_day_names, period_block_names, to_string=True):
    """Assign each rotation day a set of blocks equal to the number of periods per day."""
    blocks_of_the_day = {}
    block_cutoff = periods_per_day
    for i in range(len(rotation_day_names)):
        blocks_of_the_day[f"{rotation_day_names[i]}"] = period_block_names[i * periods_per_day:block_cutoff]
        block_cutoff += periods_per_day

    if not to_string:
        return blocks_of_the_day
    # Instead of having the values for each key (rotation day) be a list, join it to be a comma separated string.
    # By doing this, the school year dataframe can be exploded. This will eventually lead to every row in the dataframe
    # being a separate event, one for each unique period that a teacher teaches.
    # The funny thing is, when using the Pandas explode function, a list is needed, but a list can't be added to
    # the dataframe (at least I keep getting errors when trying to do it the way I have been). The workaround for now
    # is to cut the periods list into smaller lists for each rotation day, change that list to a string, add that string
    # to a column, then change that string back to a list, then explode the list... Surely there is a better way.
    else:
        for key in blocks_of_the_day:
            blocks_of_the_day[key] = ','.join(blocks_of_the_day[key])
        return blocks_of_the_day


def identify_all_periods_n(periods_per_day, list_blocks_of_the_day):
    periods_of_the_rotation = {}
    period_number = 1
    for periods in range(periods_per_day):
        periods_of_the_rotation[f"Period {period_number}"] = []
        for day, period in list_blocks_of_the_day.items():
            periods_of_the_rotation[f"Period {period_number}"].append(period[periods])
        period_number += 1
    return periods_of_the_rotation


def set_start_times(merged, periods_of_the_rotation, time_schedule):
    period_to_start_time = [
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 1"][0]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 1"][1]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 1"][2]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 1"][3]))),
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 2"][0]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 2"][1]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 2"][2]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 2"][3]))),
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 3"][0]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 3"][1]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 3"][2]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 3"][3]))),
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 4"][0]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 4"][1]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 4"][2]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 4"][3]))),
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 5"][0]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 5"][1]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 5"][2]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 5"][3]))),
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 6"][0]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 6"][1]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 6"][2]) |
         (merged['StartTime'] == periods_of_the_rotation["Period 6"][3]))),

    ]
    start_times = [time_schedule["Period 1"][0].time(), time_schedule["Period 2"][0].time(),
                   time_schedule["Period 3"][0].time(), time_schedule["Period 4"][0].time(),
                   time_schedule["Period 5"][0].time(), time_schedule["Period 6"][0].time(), ]

    merged["StartTime"] = np.select(period_to_start_time, start_times, default=merged["StartTime"])


def set_end_times(merged, periods_of_the_rotation, time_schedule):
    period_to_end_time = [
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 1"][0]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 1"][1]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 1"][2]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 1"][3]))),
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 2"][0]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 2"][1]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 2"][2]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 2"][3]))),
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 3"][0]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 3"][1]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 3"][2]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 3"][3]))),
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 4"][0]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 4"][1]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 4"][2]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 4"][3]))),
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 5"][0]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 5"][1]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 5"][2]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 5"][3]))),
        ((merged['WeekDay'] != 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 6"][0]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 6"][1]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 6"][2]) |
         (merged['EndTime'] == periods_of_the_rotation["Period 6"][3]))),

    ]
    end_times = [time_schedule["Period 1"][1].time(), time_schedule["Period 2"][1].time(),
                 time_schedule["Period 3"][1].time(), time_schedule["Period 4"][1].time(),
                 time_schedule["Period 5"][1].time(), time_schedule["Period 6"][1].time(), ]

    merged["EndTime"] = np.select(period_to_end_time, end_times, default=merged["EndTime"])


def set_tuesday_start_times(merged, periods_of_the_rotation, time_schedule):
    period_to_start_time = [
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 1"][0]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 1"][1]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 1"][2]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 1"][3]))),
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 2"][0]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 2"][1]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 2"][2]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 2"][3]))),
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 3"][0]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 3"][1]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 3"][2]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 3"][3]))),
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 4"][0]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 4"][1]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 4"][2]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 4"][3]))),
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 5"][0]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 5"][1]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 5"][2]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 5"][3]))),
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['StartTime'] == periods_of_the_rotation["Period 6"][0]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 6"][1]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 6"][2]) |
          (merged['StartTime'] == periods_of_the_rotation["Period 6"][3]))),

    ]
    tuesday_start_times = [time_schedule["Period 1"][0].time(), time_schedule["Period 2"][0].time(),
                   time_schedule["Period 3"][0].time(), time_schedule["Period 4"][0].time(),
                   time_schedule["Period 5"][0].time(), time_schedule["Period 6"][0].time(), ]

    merged["StartTime"] = np.select(period_to_start_time, tuesday_start_times, default=merged["StartTime"])


def set_tuesday_end_times(merged, periods_of_the_rotation, time_schedule):
    period_to_end_time = [
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 1"][0]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 1"][1]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 1"][2]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 1"][3]))),
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 2"][0]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 2"][1]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 2"][2]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 2"][3]))),
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 3"][0]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 3"][1]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 3"][2]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 3"][3]))),
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 4"][0]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 4"][1]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 4"][2]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 4"][3]))),
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 5"][0]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 5"][1]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 5"][2]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 5"][3]))),
        ((merged['WeekDay'] == 'Tuesday') &
         ((merged['EndTime'] == periods_of_the_rotation["Period 6"][0]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 6"][1]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 6"][2]) |
          (merged['EndTime'] == periods_of_the_rotation["Period 6"][3]))),

    ]
    tuesday_end_times = [time_schedule["Period 1"][1].time(), time_schedule["Period 2"][1].time(),
                 time_schedule["Period 3"][1].time(), time_schedule["Period 4"][1].time(),
                 time_schedule["Period 5"][1].time(), time_schedule["Period 6"][1].time(), ]

    merged["EndTime"] = np.select(period_to_end_time, tuesday_end_times, default=merged["EndTime"])
