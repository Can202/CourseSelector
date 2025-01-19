from func import * 
import numpy as np

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5


# Look between two "section"s and check if they have some conflict.
def sections_conflict(*, section_schedule_1="", section_schedule_2=""):
    section_schedule_1_in_array = get_schedule_number_array(section_schedule_1)
    section_schedule_2_in_array = get_schedule_number_array(section_schedule_2)
    return schedule_number_array_conflict(section_schedule_1_in_array, section_schedule_2_in_array)

# ###
def parse_course_info(*,text =""):
    text_split_with_spaces = text.split(" ")
    text_split = [element for element in text_split_with_spaces if element]
    dic = {}

    for i in range(len(text_split)):
        tsa = text_split[i].split("/")
        
        if tsa[0] == "###":
            return {"fail":True, "len":0}
        dic[f"{i}_type"] = tsa[0]
        daysC = tsa[1].split(":")[0].split("-")
        days = []
        for j in range(len(daysC)):
            days.append(daysC[j])
        dic[f"{i}_days"] = days
        
        hoursC = tsa[1].split(":")[1].split("-")
        hours = []
        for j in range(len(hoursC)):
            hours.append(hoursC[j])
        dic[f"{i}_hours"] = hours
    dic["len"] = len(text_split)
    dic["fail"] = False
    return dic

# Get an "schedule array"
def get_schedule_array(schedule):

    array = [[""] * 6 for _ in range(9)]
    schedule_segment = schedule.split(" ")
    schedule_segment_list_splitted = []
    DETAIL = 1
    TYPE = 0
    DAYS = 0
    HOURS = 1
    for i in range(len(schedule_segment)):
        schedule_segment_list_splitted.append(schedule_segment[i].split("/"))

    for i in range(len(schedule_segment_list_splitted)):
        detail_splitted = (schedule_segment_list_splitted[i][DETAIL]).split(":")
        days_list = detail_splitted[DAYS].split("-")
        hours_list = detail_splitted[HOURS].split("-")
        days_number_list = []
        for j in range(len(days_list)):
            days_number_list.append(get_day_from_Letter(days_list[j]))
        for j in range(len(days_number_list)):
            for k in range(len(hours_list)):
                array[int(hours_list[k])-1][days_number_list[j]] = schedule_segment_list_splitted[i][TYPE]
    return array

# Get an "schedule number array"
def get_schedule_number_array(schedule):
    schedule_number_array = np.zeros((9, 6), dtype=int)  # 9 hours, 6 days
    for schedule_segment in schedule.split(" "):
        if not schedule_segment:
            continue
        schedule_segment_type, schedule_segment_detail = schedule_segment.split("/")
        days_dash, hours_dash = schedule_segment_detail.split(":")
        days_number_list = [get_day_from_Letter(day) for day in days_dash.split("-")]
        hours_list = [int(hour) - 1 for hour in hours_dash.split("-")]
        for day_number in days_number_list:
            for hour in hours_list:
                schedule_number_array[hour, day_number] = 1  # Mark as occupied
    return schedule_number_array

# Look between "schedule number array"s of two sections and check if they have some conflict.
def schedule_number_array_conflict(array1, array2):
    return np.any(array1 & array2)

# ### Look between two courses and check if they have some conflict hour/day (in Dict format). 
def dict_courses_conflict(*, dict1, dict2):

    conflict_in_days, conflict_in_hours = False, False

    for i in range(dict1["len"]):
        for j in range(dict2["len"]):
            conflict_in_days = dicts_have_same(dict1[f"{i}_days"], dict2[f"{j}_days"])
            conflict_in_hours = dicts_have_same(dict1[f"{i}_hours"], dict2[f"{j}_hours"])

            if conflict_in_days and conflict_in_hours:
                return True
    return False

# ### Check if two lists of the dict have something in common. 
def dicts_have_same(dict1_list, dict2_list):
    for i in range(len(dict1_list)):
        if dict1_list[i] in ''.join(map(str, dict2_list)):
            return True
    return False

# ###
def get_data():
    raw_data = csv_reader(path_file="data.csv")
    return plain_text_to_array(data=raw_data)

# ### from a calendar in a specific day and hour, get the class. 
def what_is(day, hour, calendar):
    for i in range(len(calendar["sections_schedule"])):
        dic = parse_course_info(text=calendar["sections_schedule"][i])
        for j in range(dic["len"]):
            if (day in dic[f"{j}_days"]) and (str(hour) in dic[f"{j}_hours"]):
                return f"{dic[f'{j}_type']} {calendar['courses_id'][i]}"
    return ""
    
# ### This prints the calendar in a readable way. 
def calendar_show(calendar, PRINT = True):
    len_between_columns = 19
    hour_options = 10
    day_options = 6
    start_hour_counter = 0
    start_day_counter = -1 # day 0 is MONDAY, so to print first a column with the hours, we need to start at -1
    text= ""

    if PRINT:
        print()
    text += "\n"
    for hour in range(start_hour_counter, hour_options):
        for day in range(start_day_counter, day_options):
            if day == start_day_counter:
                if PRINT:
                    print(f"{hour} ", end="")
                text += f"{hour} "
            elif hour == start_hour_counter:
                str_day = get_day(day)
                if PRINT:
                    print(str_day.center(len_between_columns), end="")
                text += str_day.center(len_between_columns)
            else:
                str_class = what_is(get_day(day),hour,calendar)
                if PRINT:
                    print(str_class.center(len_between_columns), end="")
                text += str_class.center(len_between_columns)
            if PRINT:
                print("|", end="")
            text += "|"
        if PRINT:
            print()
        text += "\n"
    if PRINT:
        print()
    text += "\n"

# ###
def get_day(day):
    if day==MONDAY:
        return 'L'
    if day==TUESDAY:
        return 'M'
    if day==WEDNESDAY:
        return 'W'
    if day==THURSDAY:
        return 'J'
    if day==FRIDAY:
        return 'V'
    if day==SATURDAY:
        return 'S'

# ###
def get_day_from_Letter(day):
    if day=='L':
        return MONDAY
    if day=='M':
        return TUESDAY
    if day=='W':
        return WEDNESDAY
    if day=='J':
        return THURSDAY
    if day=='V':
        return FRIDAY
    if day=='S':
        return SATURDAY