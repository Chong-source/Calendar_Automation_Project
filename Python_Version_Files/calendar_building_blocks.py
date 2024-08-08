
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


def assign_block_names_to_periods(periods_per_day, rotation_day_names, period_block_names):
    blocks_of_the_day = {}
    block_cutoff = periods_per_day
    for i in range(len(rotation_day_names)):
        blocks_of_the_day[f"{rotation_day_names[i]}"] = period_block_names[i * periods_per_day:block_cutoff]
        block_cutoff += periods_per_day

    return blocks_of_the_day
