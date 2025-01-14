# Constants
ROW_SKIP = 0
COLUMN_SKIP = 1
from func import *
from parsing import *
import time

def get_all_calendars(data):
    # Options
    courses_quantity = len(data) - 1
    courses_id = []
    courses_options = []
    for i in range(courses_quantity):
        courses_options.append(count_options(data[i]))
        courses_id.append(i)
    courses_quantity, [courses_id] = many_sorts(courses_options, [courses_id])

    the_calendars = all_calendars(data, courses_id, courses_options)
    return the_calendars

def all_calendars(data, courses_id, courses_options):
    start_time = time.time()

    n = variation(courses_options)
    raw_list_of_complete_calendars = raw_list_of_all_calendars(data, courses_id, courses_options)

    # Remove duplicates
    raw_list_of_unique_complete_calendars = []
    for i in range(len(raw_list_of_complete_calendars)):
        add = True
        for j in range(len(raw_list_of_unique_complete_calendars)):
            if raw_list_of_complete_calendars[i] == raw_list_of_unique_complete_calendars[j]:
                add = False
        if add:
            raw_list_of_unique_complete_calendars.append(raw_list_of_complete_calendars[i])

    # Remove calendars that have conflict
    the_calendars = []
    for i in range(len(raw_list_of_unique_complete_calendars)):
        if not is_calendar_with_conflicts(raw_list_of_unique_complete_calendars[i]):
            Debug(f"Check for conflicts for calendar {i}, but didn't found any")
            the_calendars.append(raw_list_of_unique_complete_calendars[i])
        else:
            Debug(f"Check for conflicts for calendar {i}, found them")
            Debug(f"-------------------------")
        


    Debug("---Calendars---")
    for i in range(len(the_calendars)):
        Debug(f"---Calendar {i+1}---")
        Debug(the_calendars[i])
        if DEBUG:
            calendar_show(the_calendars[i])

    Debug(f"Calendars Calculated: {n}")
    Debug(f"Calendars w/o conflicts: {len(the_calendars)}")
    Debug(f"--- {(time.time() - start_time)} seconds ---", True)
    return the_calendars

def is_calendar_with_conflicts(calendar):
    n = len(calendar["calendar"])
    conflict = False
    for i in range(n):
        for j in range(i+1, n):
            if courses_conflict(first_schedule_in_str=calendar["calendar"][i], second_schedule_in_str=calendar["calendar"][j]):
                conflict = True
    return conflict


# Function that redoes the make_calendar functionality
def raw_list_of_all_calendars(data, courses_id, courses_options):
    list_of_calendars = []
    n = variation(courses_options)
    for i in range(n):
        new_calendar = {"calendar":[], "name":[]}

        combinations = courses_combination(courses_options, i)

        for j in range(len(courses_id)):
            id = courses_id[j]
            selection = combinations[j]
            Debug(f"{id}: ---{data[id][0]}---")

            new_calendar["name"].append(data[id][0])
            new_calendar["calendar"].append(data[id][selection])

        Debug("---NEXT---")
        list_of_calendars.append(new_calendar)
    return list_of_calendars

def courses_combination(courses_options, attempt):
    n = len(courses_options)
    combination = [1] * n
    if attempt == 0:
        return combination
        
    level = n
    divisor=99999999

    while level > 0:
        if attempt == 0:
            level = -500
            continue
        while attempt < divisor:
            if level < 0:
                return -1
            level -= 1
            divisor=1
            for i in range(1, level+1):
                divisor *= courses_options[-i]
        
        division = attempt // divisor
        combination[-(level+1)] += division
        attempt = attempt % divisor
    
    return combination


def count_options(row_data):
    count = 0
    for temp in range(len(row_data) - COLUMN_SKIP):
        i = temp + COLUMN_SKIP
        if row_data[i] != "":
            count += 1
    return count

