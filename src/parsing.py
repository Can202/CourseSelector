from func import * 

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5

# Look between two courses and check if they have some conflict hour/day (in str).
def courses_conflict(*,first_schedule_in_str ="", second_schedule_in_str=""):
    dic_1 = parse_course_info(text = first_schedule_in_str)
    dic_2 = parse_course_info(text = second_schedule_in_str)
    return dict_courses_conflict(dict1=dic_1, dict2=dic_2)

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

# Look between two courses and check if they have some conflict hour/day (in Dict format).
def dict_courses_conflict(*, dict1, dict2):

    conflit_in_days, conflit_in_hours = False, False

    for i in range(dict1["len"]):
        for j in range(dict2["len"]):
            conflit_in_days = dicts_have_same(dict1[f"{i}_days"],dict2[f"{j}_days"])
            conflit_in_hours = dicts_have_same(dict1[f"{i}_hours"],dict2[f"{j}_hours"])

            if conflit_in_days and conflit_in_hours:
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
    
# This prints the calendar in a readable way.
def calendar_show(calendar):
    print()
    for i in range(10):
        for k in range(7):
            j = k-1
            if j == -1:
                print(f"{i} ",end="")
            elif i != 0:
                s = what_is(get_day(j),i,calendar)
                print(s.ljust(20), end="")
            else:
                s = get_day(j)
                print(s.ljust(20), end="")
            print("|", end="")
        print()
    print()
