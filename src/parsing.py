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
def get_section_schedule_dict(*,section_schedule =""):
    text_split_with_spaces = section_schedule.split(" ")
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
            days_number_list.append(get_day_number(days_list[j]))
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
        days_number_list = [get_day_number(day) for day in days_dash.split("-")]
        hours_list = [int(hour) - 1 for hour in hours_dash.split("-")]
        for day_number in days_number_list:
            for hour in hours_list:
                schedule_number_array[hour, day_number] = 1  # Mark as occupied
    return schedule_number_array

# Look between "schedule number array"s of two sections and check if they have some conflict.
def schedule_number_array_conflict(array1, array2):
    return np.any(array1 & array2)

# Get main_data
def get_main_data():
    raw_main_data = csv_reader(path_file="data.csv")
    return get_data_from_raw_data(raw_data=raw_main_data)

# Get "section_class_on_time" from a calendar in a specific day and hour.
def get_section_class_on_time(*, calendar, day, hour):
    for i in range(len(calendar["sections_schedule"])):
        section_schedule_dict = get_section_schedule_dict(section_schedule=calendar["sections_schedule"][i])
        for j in range(section_schedule_dict["len"]):
            if (day in section_schedule_dict[f"{j}_days"]) and (str(hour) in section_schedule_dict[f"{j}_hours"]):
                return f"{section_schedule_dict[f'{j}_type']} {calendar['courses_id'][i]}"
    return ""
    
# This prints the calendar in a readable way.
def calendar_show(calendar, PRINT = True):
    len_between_columns = 17
    hour_options = 10
    day_options = 6
    start_hour_counter = 0
    start_day_counter = -1 # day 0 is MONDAY, so to print first a column with the hours, we need to start at -1
    text= ""

    if PRINT:
        print()
    text += "\n"
    for hour in range(start_hour_counter, hour_options):
        for day_number in range(start_day_counter, day_options):
            if day_number == start_day_counter:
                if PRINT:
                    print(f"{hour} ", end="")
                text += f"{hour} "
            elif hour == start_hour_counter:
                day = get_day(day_number)
                if PRINT:
                    print(day.center(len_between_columns), end="")
                text += day.center(len_between_columns)
            else:
                section_class_on_time = get_section_class_on_time(calendar=calendar,day=get_day(day_number),hour=hour)
                if PRINT:
                    print(section_class_on_time.center(len_between_columns), end="")
                text += section_class_on_time.center(len_between_columns)
            if PRINT:
                print("|", end="")
            text += "|"
        if PRINT:
            print()
        text += "\n"
    if PRINT:
        print()
    text += "\n"
    return text

# Get day from day number
def get_day(day_number):
    if day_number==MONDAY:
        return 'L'
    if day_number==TUESDAY:
        return 'M'
    if day_number==WEDNESDAY:
        return 'W'
    if day_number==THURSDAY:
        return 'J'
    if day_number==FRIDAY:
        return 'V'
    if day_number==SATURDAY:
        return 'S'

# Get day number from day
def get_day_number(day):
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