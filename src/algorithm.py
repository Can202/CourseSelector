# Constants
ROW_SKIP = 0
COLUMN_SKIP = 1
from func import *
from parsing import *
import pointsys
import cache
import time
import re

# Main functions
def get_calendars_from_data(main_data, progress_callback=None):

    # Check if main_data is in cache
    saving = False
    cache_number = cache.in_cache()
    if cache_number != 0:
        print("Found the calendars in your cache. Loaded from there.")
        calendars, points = cache.load_cache(number=cache_number)
        loadingAnimation(done=True,progress_callback=progress_callback)
        return calendars, points, True
    else:
        saving = True

    # Options
    if main_data[-1] == ['']:
        main_data = remove_by_index(main_data, -1)
    
    courses_quantity = len(main_data)
    courses_index = []
    courses_sections_quantity = []
    for i in range(courses_quantity):
        courses_sections_quantity.append(count_options(main_data[i]))
        courses_index.append(i)
    
    courses_quantity, [courses_index] = sort_many_lists_by_ascending_order_of_one_list(courses_sections_quantity, [courses_index])

    calendars, points = all_calendars_with_courses_extra_info(main_data, courses_index, courses_sections_quantity, progress_callback)

    if saving:
        cache.save_cache(main_data, calendars, points)

    return calendars, points, False


def all_calendars_with_courses_extra_info(main_data, courses_index, courses_sections_quantity, progress_callback=None):
    start_time = time.time()

    debug_total = multiplication_of_each_element(courses_sections_quantity)

    # Create list of posible calendars (p.1)
    calendars = raw_list_of_all_calendars(main_data, courses_index, courses_sections_quantity, progress_callback)

    # Remove calendars that have conflict (p.2)
    calendars = remove_calendars_with_conflict(calendars,progress_callback)
    debug_woconflict = len(calendars)

    if debug_woconflict != 0:
        # Mark NRC with professors banned (p.3)
        if calendars[0]["nrc_active"]:
            calendars = mark_NRC_with_professors_banned(calendars,progress_callback)
        # Combine calendars with the same schedule (p.4)
        calendars = combine_NRC_for_exact_schedule(calendars, calendars[0]["nrc_active"],progress_callback)

        # Add nrc alternatives to the calendars (p.5)
        if calendars[0]["nrc_active"]:
            calendars = check_NRC_alternatives(calendars, main_data,progress_callback)

    # Point system (p.6)
    if len(calendars) == 0:
        return calendars, []
    points = pointsys.point_system(calendars,progress_callback)
    [points, [calendars]] = sort_many_lists_by_descending_order_of_one_list(points, [calendars])

    loadingAnimation(done=True,progress_callback=progress_callback)

    Debug(f"Calendars Calculated: {debug_total}")
    Debug(f"Calendars w/o conflicts: {debug_woconflict}")
    Debug(f"Calendars w/o repetition nor conflicts: {len(calendars)}")

    Debug(f"--- {(time.time() - start_time)} seconds ---", ignore_debug_statement=True)
    return calendars, points


def get_list_of_banned_profs():
    if not os.path.exists("professors_banned.txt"):
        return [""]
    raw_list = csv_reader(path_file="professors_banned.txt")
    a = raw_list.split("\n")
    list_of_banned_profs = []
    for i in range(len(a)):
        if a[i] !="":
            list_of_banned_profs.append(a[i])

    return list_of_banned_profs

def mark_NRC_with_professors_banned(calendars, progress_callback=None):
    list_of_banned_profs = get_list_of_banned_profs()
    for i in range(len(calendars)):
        loadingAnimation(part=3, i=i, n=len(calendars),progress_callback=progress_callback)
        for k in range(len(calendars[i]["profs"])):
            banned = False
            for q in range(len(calendars[i]["profs"][k])):
                if calendars[i]["profs"][k][q] in list_of_banned_profs:
                    banned = True
            if banned:
                calendars[i]["sections_nrc_bundle"][k] = "!" + calendars[i]["sections_nrc_bundle"][k] + "!"
    return calendars



def remove_calendars_with_conflict(calendars,progress_callback=None):
    new_calendars = []
    for i in range(len(calendars)):
        loadingAnimation(part=2, i=i, n=len(calendars),progress_callback=progress_callback)
        if not is_calendar_with_conflicts(calendars[i]):
            Debug(f"Check for conflicts for calendar {i}, but didn't found any")
            new_calendars.append(calendars[i])
        else:
            Debug(f"Check for conflicts for calendar {i}, found them")
            Debug(f"-------------------------")
    return new_calendars
    
def combine_NRC_for_exact_schedule(calendars, NRC_active,progress_callback=None):
    n = len(calendars)
    i = 0
    while i < n:
        j = i+1
        loadingAnimation(part=4, i=i, n=n,progress_callback=progress_callback)
        while j < n:
            if two_calendars_have_the_same_schedule(calendars[i], calendars[j]):
                if NRC_active:
                    calendars[i]["sections_nrc_bundle"] = combine_NRCs(calendars[i], calendars[j])
                calendars = remove_by_index(calendars, j)
                j-=1
                n = len(calendars)
            j+=1
        i+=1
    return calendars

def two_calendars_have_the_same_schedule(calendar1, calendar2):
    for i in range(len(calendar1["sections_schedule"])):
        if not two_sections_have_the_same_schedule(calendar1["sections_schedule"][i], calendar2["sections_schedule"][i]):
            return False
    return True

def two_sections_have_the_same_schedule(section1, section2):
    if section1 == section2:
        return True
    course1list = section1.split(" ")
    course2list = section2.split(" ")
    if sorted(course1list) == sorted(course2list):
        return True
    if get_schedule_array(section1) == get_schedule_array(section2):
        return True
    return False

def combine_NRCs(calendar1, calendar2):
    nrc1 = calendar1["sections_nrc_bundle"]
    nrc2 = calendar2["sections_nrc_bundle"]
    for i in range(len(nrc1)):
        name = ""
        if calendar2["courses_id"][i] != calendar1["courses_id"][i]:
            name = calendar2["courses_id"][i] + ": "
        if not (nrc2[i] in nrc1[i]):
            nrc1[i] += ("/" + name + nrc2[i])
    return nrc1

def check_NRC_alternatives(calendars, main_data,progress_callback=None):
    for index in range(len(calendars)):
        loadingAnimation(part=5, i=index, n=len(calendars),progress_callback=progress_callback)
        for j in range(len(main_data)):
            for k in range(1,len(main_data[j])):
                if main_data[j][k] == "":
                    continue
                add = True
                updater = 0
                for i in range(len(calendars[index]["sections_schedule"])):
                    if main_data[j][0] == calendars[index]["courses_bundle_id"][i]:
                        updater = i
                        continue
                    if sections_conflict(section_schedule_1=calendars[index]["sections_schedule"][i], section_schedule_2=get_schedule_from_section_info(main_data[j][k])):
                        add = False
                if add:
                    nrc = ""
                    name = ""
                    profs_str = ""
                    if is_Prof_on(main_data[j][k]):
                        profs_str, a = get_profs_and_remaining_info_from_section_info(main_data[j][k])
                    else:
                        a = main_data[j][k]
                    if is_NRC_on(a):
                        nrc, a = get_NRC_and_remaining_info_from_section_info(main_data[j][k])
                    if is_customName_on(a):
                        name, a = get_customName_and_remaining_info_from_section_info(a)

                    if not(nrc in calendars[index]["sections_nrc_bundle"][updater]):
                        if name == calendars[index]["courses_id"][updater]:
                            name = ""
                        if name != "":
                            name += ": "
                        if calendars[index]["sections_nrc_alternative_bundle"][updater] != "":
                            calendars[index]["sections_nrc_alternative_bundle"][updater] += "/" + name + nrc
                        else:
                            calendars[index]["sections_nrc_alternative_bundle"][updater] += name + nrc
    return calendars

# Function that check if a calendar has conflicts. It is used in all_calendars function to remove the ones with conflicts.
def is_calendar_with_conflicts(calendar):
    sections_schedule = sorted(calendar["sections_schedule"], key=len, reverse=True)
    n = len(sections_schedule)
    for i in range(n):
        for j in range(i+1, n):
            if sections_conflict(section_schedule_1=sections_schedule[i], section_schedule_2=sections_schedule[j]):
                return True
    return False


# Function that return all the posible calendar combinations, ignoring repetition, conflicts, etc. It is used in all_calendars, where the calendar list is cleaned with other functions
def raw_list_of_all_calendars(main_data, courses_index, courses_sections_quantity, progress_callback=None):
    calendars = []
    n = multiplication_of_each_element(courses_sections_quantity)
    nrc_active = True

    for i in range(n):
        loadingAnimation(part=1, i=i, n=n, progress_callback=progress_callback)
        new_calendar = {"sections_schedule":[], "courses_id":[], "sections_nrc_bundle":[], "nrc_active": True, "sections_nrc_alternative_bundle": [], "courses_bundle_id":[], "profs":[]}

        combinations = courses_combination(courses_sections_quantity, i)

        for j in range(len(courses_index)):
            id = courses_index[j]
            selection = combinations[j]

            
            name = main_data[id][0]
            section_info = main_data[id][selection]
            nrc = "###"
            profs_str = ""

            if is_Prof_on(section_info):
                profs_str, section_info = get_profs_and_remaining_info_from_section_info(section_info)
            if is_NRC_on(section_info):
                nrc, section_info = get_NRC_and_remaining_info_from_section_info(section_info)
            else:
                nrc_active = False

                
            if is_customName_on(section_info):
                name, section_info = get_customName_and_remaining_info_from_section_info(section_info)
            
            new_calendar["sections_nrc_bundle"].append(nrc)
            new_calendar["sections_nrc_alternative_bundle"].append("")
            new_calendar["courses_id"].append(name)
            new_calendar["courses_bundle_id"].append(main_data[id][0])
            new_calendar["sections_schedule"].append(section_info)
            new_calendar["profs"].append(profs_str.split("/"))

        calendars.append(new_calendar)

    for i in range(len(calendars)):
        calendars[i]["nrc_active"] = nrc_active

    return calendars

# Function used to get combination of posible calendars with only one number identifier. It is used in the raw_list_of_all_calendars function.
# For example, the identifier 55 makes the selection of courses [5,3,5,2,6,3]. So that means that the first course is going to be the section 5, and so on.
# The identifier 56 makes [5,3,5,2,6,4] and maybe the identifier 57 makes [5,3,5,2,7,1], etc.
def courses_combination(courses_sections_quantity, attempt):
    n = len(courses_sections_quantity)
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
                divisor *= courses_sections_quantity[-i]
        
        division = attempt // divisor
        combination[-(level+1)] += division
        attempt = attempt % divisor
    return combination

def get_schedule_from_section_info(section_info):
    if is_Prof_on(section_info):
        a, section_info = get_profs_and_remaining_info_from_section_info(section_info)
    if is_NRC_on(section_info):
        a, section_info = get_NRC_and_remaining_info_from_section_info(section_info)
    if is_customName_on(section_info):
        a, section_info = get_customName_and_remaining_info_from_section_info(section_info)
    return section_info

def is_Prof_on(section_info):
    return "(" in section_info

def get_profs_and_remaining_info_from_section_info(section_info):
    index_start, index_end = string_between_two_substrings("(",")",section_info)
    return section_info[index_start:index_end], section_info[:(index_start-2)]+section_info[(index_end+1):]


def is_NRC_on(section_info):
    return "$" in section_info

def get_NRC_and_remaining_info_from_section_info(section_info):
    match = re.search(r"\$(\d+)", section_info)
    if match:
        number = match.group(1)
        remaining_text = section_info.replace(match.group(0), "").strip()
    return str(number), remaining_text

def is_customName_on(section_info):
    return "%" in section_info

def get_customName_and_remaining_info_from_section_info(section_info):
    match = re.search(r"%([a-zA-Z0-9_]+)", section_info)
    if match:
        name = match.group(1)
        remaining_text = section_info.replace(match.group(0), "").strip()
    return str(name), remaining_text

def count_options(row_data):
    count = 0
    for temp in range(len(row_data) - COLUMN_SKIP):
        i = temp + COLUMN_SKIP
        if row_data[i] != "":
            count += 1
    return count

