# The parse
from func import * 

def courses_conflict(*,text1 ="", text2=""):
    dic1 = parse_course_info(text =text1)
    dic2 = parse_course_info(text =text2)
    return dict_courses_conflict(dict1=dic1, dict2=dic2)
def parse_course_info(*,text =""):
    ts = text.split(" ")
    dic = {}
    for i in range(len(ts)):
        tsa = ts[i].split("/")
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
    return dic

def dict_courses_conflict(*, dict1, dict2):
    conflit_in_days= False
    conflit_in_hours= False
    for i in range(dict1["len"]):
        for j in range(dict2["len"]):
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