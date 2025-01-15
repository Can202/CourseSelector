# Constants
ROW_SKIP = 0
COLUMN_SKIP = 1
from func import *
from parsing import *
import time
import re


# Function that only uses the data input to get all the calendars, using all_calendars function. 
# This function maybe could be removed, as it now has something that isn't needed anymore, the special sorting
# by quantity that it was used to save time in the old algorithm.
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


# Function that returns the calendars without conflicts
def all_calendars(data, courses_id, courses_options):
    start_time = time.time()

    n = variation(courses_options)

    # Create list of posible calendars (p.1)
    the_calendars = raw_list_of_all_calendars(data, courses_id, courses_options)

    # Remove duplicates (p.2)
    the_calendars = remove_duplicates_of_calendars(the_calendars)

    # Remove calendars that have conflict (p.3)
    the_calendars = remove_calendars_with_conflict(the_calendars)
    woconflict = len(the_calendars)

    # Combine calendars with the same schedule (p.4)
    if the_calendars[0]["nrc_active"]:
        the_calendars = combine_NRC_for_exact_schedule(the_calendars)

    loadingAnimation(done=True)

    Debug("---Calendars---")
    for i in range(len(the_calendars)):
        Debug(f"---Calendar {i+1}---")
        Debug(the_calendars[i])
        if DEBUG:
            calendar_show(the_calendars[i])

    Debug(f"Calendars Calculated: {n}")
    Debug(f"Calendars w/o conflicts: {woconflict}")
    Debug(f"Calendars w/o repetition nor conflicts: {len(the_calendars)}")
    Debug(f"--- {(time.time() - start_time)} seconds ---", ignore_debug_statement=True)
    return the_calendars

def remove_duplicates_of_calendars(calendars):
    the_calendars = []
    ln = len(calendars)
    for i in range(ln):
        loadingAnimation(part=2, i=i, n=ln)
        add = True
        for j in range(len(the_calendars)):
            if calendars[i] == the_calendars[j]:
                add = False
        if add:
            the_calendars.append(calendars[i])
    return the_calendars

def remove_calendars_with_conflict(calendars):
    the_calendars = []
    for i in range(len(calendars)):
        loadingAnimation(part=3, i=i, n=len(calendars))
        if not is_calendar_with_conflicts(calendars[i]):
            Debug(f"Check for conflicts for calendar {i}, but didn't found any")
            the_calendars.append(calendars[i])
        else:
            Debug(f"Check for conflicts for calendar {i}, found them")
            Debug(f"-------------------------")
    return the_calendars
    
def combine_NRC_for_exact_schedule(calendars):
    n = len(calendars)
    i = 0
    while i < n:
        j = i+1
        loadingAnimation(part=4, i=i, n=n)
        while j < n:
            if two_calendars_have_the_same_schedule(calendars[i], calendars[j]):
                calendars[i]["nrc"] = combine_NRCs(calendars[i]["nrc"], calendars[j]["nrc"])
                calendars = remove_by_index(calendars, j)
                j-=1
                n = len(calendars)
            j+=1
        i+=1
    return calendars

def two_calendars_have_the_same_schedule(calendar1, calendar2):
    for i in range(len(calendar1["calendar"])):
        if not two_courses_have_the_same_schedule(calendar1["calendar"][i], calendar2["calendar"][i]):
            return False
    return True
def two_courses_have_the_same_schedule(course1, course2):
    if course1 == course2:
        return True
    course1list = course1.split(" ")
    course2list = course2.split(" ")
    if sorted(course1list) == sorted(course2list):
        return True
    if get_days_array(course1) == get_days_array(course2):
        return True
    return False

def combine_NRCs(nrc1, nrc2):
    for i in range(len(nrc1)):
        if not (nrc2[i] in nrc1[i]):
            nrc1[i] += ("/" + nrc2[i])
    return nrc1

# Function that check if a calendar has conflicts. It is used in all_calendars function to remove the ones with conflicts.
def is_calendar_with_conflicts(calendar):
    n = len(calendar["calendar"])
    conflict = False
    for i in range(n):
        for j in range(i+1, n):
            if courses_conflict(first_schedule_in_str=calendar["calendar"][i], second_schedule_in_str=calendar["calendar"][j]):
                conflict = True
    return conflict


# Function that return all the posible calendar combinations, ignoring repetition, conflicts, etc. It is used in all_calendars, where the calendar list is cleaned with other functions
def raw_list_of_all_calendars(data, courses_id, courses_options):
    list_of_calendars = []
    n = variation(courses_options)
    nrc_active = True

    for i in range(n):
        loadingAnimation(part=1, i=i, n=n)
        new_calendar = {"calendar":[], "name":[], "nrc":[], "nrc_active": True}

        combinations = courses_combination(courses_options, i)

        for j in range(len(courses_id)):
            id = courses_id[j]
            selection = combinations[j]
            Debug(f"{id}: ---{data[id][0]}---")

            
            name = data[id][0]
            info = data[id][selection]
            nrc = "###"

            if is_NRC_on(info):
                nrc, info = get_NRC_and_course_info(info)
            else:
                nrc_active = False

                
            if is_customName_on(info):
                name, info = get_customName_and_course_info(info)
            
            new_calendar["nrc"].append(nrc)
            new_calendar["name"].append(name)
            new_calendar["calendar"].append(info)
                
            Debug(f"--- Done ---")

        Debug("---NEXT---")
        list_of_calendars.append(new_calendar)

    for i in range(len(list_of_calendars)):
        list_of_calendars[i]["nrc_active"] = nrc_active

    return list_of_calendars

# Function used to get combination of posible calendars with only one number identifier. It is used in the raw_list_of_all_calendars function.
# For example, the identifier 55 makes the selection of courses [5,3,5,2,6,3]. So that means that the first course is going to be the section 5, and so on.
# The identifier 56 makes [5,3,5,2,6,4] and maybe the identifier 57 makes [5,3,5,2,7,1], etc.
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


def is_NRC_on(calendar_text):
    return "$" in calendar_text

def get_NRC_and_course_info(text):
    match = re.search(r"\$(\d+)", text)
    if match:
        number = match.group(1)
        remaining_text = text.replace(match.group(0), "").strip()
    return str(number), remaining_text

def is_customName_on(calendar_text):
    return "%" in calendar_text

def get_customName_and_course_info(text):
    match = re.search(r"%([a-zA-Z0-9_]+)", text)
    if match:
        name = match.group(1)
        remaining_text = text.replace(match.group(0), "").strip()
    return str(name), remaining_text

def count_options(row_data):
    count = 0
    for temp in range(len(row_data) - COLUMN_SKIP):
        i = temp + COLUMN_SKIP
        if row_data[i] != "":
            count += 1
    return count

