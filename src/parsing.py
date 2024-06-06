# The parse
from func import * 
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5

def courses_conflict(*,text1 ="", text2=""):
    dic1 = parse_course_info(text =text1)
    dic2 = parse_course_info(text =text2)
    return dict_courses_conflict(dict1=dic1, dict2=dic2)
def parse_course_info(*,text =""):
    tsNF = text.split(" ")
    ts = [i for i in tsNF if i]
    dic = {}
    for i in range(len(ts)):
        tsa = ts[i].split("/")
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
    dic["len"] = len(ts)
    dic["fail"] = False
    return dic

def dict_courses_conflict(*, dict1, dict2):
    conflit_in_days= False
    conflit_in_hours= False
    for i in range(dict1["len"]):
        for j in range(dict2["len"]):
            conflit_in_days, conflit_in_hours = False, False
            for k in range(len(dict1[f"{i}_days"])):
                if dict1[f"{i}_days"][k] in ''.join(map(str, dict2[f"{j}_days"])):
                    conflit_in_days= True
            for k in range(len(dict1[f"{i}_hours"])):
                if dict1[f"{i}_hours"][k] in ''.join(map(str, dict2[f"{j}_hours"])):
                    conflit_in_hours= True
            if conflit_in_days and conflit_in_hours:
                return True
    return False

def get_data():
    raw_data = csv_reader(path_file="data.csv")
    return plain_text_to_array(data=raw_data)

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
