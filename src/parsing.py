from func import * 
import numpy as np

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5


# Look between two courses and check if they have some conflict hour/day (in str).

def courses_conflict(*, first_schedule_in_str="", second_schedule_in_str=""):
    array1 = get_days_array_np(first_schedule_in_str)
    array2 = get_days_array_np(second_schedule_in_str)
    return arrays_have_conflicts_np(array1, array2)

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

def get_days_array(course_str):
    array = [[""] * 6 for _ in range(9)]
    course_split = course_str.split(" ")
    course_info = []
    for i in range(len(course_split)):
        course_info.append(course_split[i].split("/"))

    for i in range(len(course_info)):
        info = (course_info[i][1]).split(":")
        days_not = info[0].split("-")
        hour = info[1].split("-")
        days = []
        for j in range(len(days_not)):
            days.append(get_day_from_Letter(days_not[j]))
        for j in range(len(days)):
            for k in range(len(hour)):
                array[int(hour[k])-1][days[j]] = course_info[i][0]

    return array

# just to mark as occupied, not containing information, this makes 1 and 0
def get_days_array_np(course_str):
    array = np.zeros((9, 6), dtype=int)  # 9 hours, 6 days
    for course in course_str.split(" "):
        if not course:
            continue
        course_type, schedule = course.split("/")
        days, hours = schedule.split(":")
        days = [get_day_from_Letter(day) for day in days.split("-")]
        hours = [int(hour) - 1 for hour in hours.split("-")]
        for day in days:
            for hour in hours:
                array[hour, day] = 1  # Mark as occupied
    return array

def arrays_have_conflicts_np(array1, array2):
    return np.any(array1 & array2)

# Look between two courses and check if they have some conflict hour/day (in Dict format).
def dict_courses_conflict(*, dict1, dict2):

    conflict_in_days, conflict_in_hours = False, False

    for i in range(dict1["len"]):
        for j in range(dict2["len"]):
            conflict_in_days = dicts_have_same(dict1[f"{i}_days"], dict2[f"{j}_days"])
            conflict_in_hours = dicts_have_same(dict1[f"{i}_hours"], dict2[f"{j}_hours"])

            if conflict_in_days and conflict_in_hours:
                return True
    return False

# Check if two lists of the dict have something in common.
def dicts_have_same(dict1_list, dict2_list):
    for i in range(len(dict1_list)):
        if dict1_list[i] in ''.join(map(str, dict2_list)):
            return True
    return False

def get_data():
    raw_data = csv_reader(path_file="data.csv")
    return plain_text_to_array(data=raw_data)

# from a calendar in a specific day and hour, get the class.
def what_is(day, hour, calendar):
    for i in range(len(calendar["calendar"])):
        dic = parse_course_info(text=calendar["calendar"][i])
        for j in range(dic["len"]):
            if (day in dic[f"{j}_days"]) and (str(hour) in dic[f"{j}_hours"]):
                return f"{dic[f'{j}_type']} {calendar['name'][i]}"
    return ""
    
# This prints the calendar in a readable way.
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