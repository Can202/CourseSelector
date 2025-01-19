from parsing import *

def point_system(the_calendars):
    points = [100] * len(the_calendars)

    data = json_reader(path_file="config.json")

    start_time=data["start_time"]
    end_time=data["end_time"]
    days=data["days"]
    hours_weight=data["weight_in_preferred_hours"]
    days_weight=data["weight_in_preferred_days"]
    
    free_module_quantity_days = data["free_module"]["quantity_days"]
    free_module_min_hours = data["free_module"]["min_hours"]
    free_module_max_hours = data["free_module"]["max_hours"]
    free_module_next_to = data["free_module"]["next_to"]
    free_module_weight = data["free_module"]["weight"]

    nrc_quantity= data["nrc"]["nrc_quantity_weight"]
    nrc_alternatives= data["nrc"]["nrc_alternatives_weight"]


    for i in range(len(the_calendars)):
        points[i] += classes_in_between_hours(the_calendars[i], start_time, end_time, hours_weight)
        points[i] += classes_in_days(the_calendars[i], days, days_weight)
        points[i] += free_modules(the_calendars[i], free_module_quantity_days, free_module_min_hours, free_module_max_hours, free_module_next_to, free_module_weight)
        points[i] += fn_nrc_quantity(the_calendars[i], nrc_quantity,nrc_alternatives)

    return points

def classes_in_between_hours(calendar, a, b, weight):
    points = 0
    for i in range(9):
        for j in range(6):
            s = what_is(get_day(j),i,calendar)
            if s != "" and not((a <= i) and (i <= b)):
                pnt = 0
                if (a <= i): 
                    pnt = abs(i-a) 
                else: 
                    pnt = abs(i-b)
                points -= pnt
    return points * weight
                
def classes_in_days(calendar, days, weight):
    points = 0
    for i in range(9):
        for j in range(6):
            s = what_is(get_day(j),i,calendar)
            if s != "" and not(get_day(j) in days):
                points -= 1
    return points * weight

def free_modules(calendar, fm_days, fm_min, fm_max, fm_next, free_module_weight):
    days = 0
    points = 0
    for j in range(6):
        len = 0
        this_day = False
        for k in range(9):
            i = k+1
            if what_is(get_day(j),i,calendar) == "":
                len += 1
                this_day = True
            else:
                points -= len
                len = 0
        if this_day:
            days +=1
    
    points -= 2 * abs(fm_days-days)

            
    return points * free_module_weight

def fn_nrc_quantity(calendar, nrc_quantity,nrc_alternatives):
    ct_nrc_quantity = 0
    ct_nrc_alternatives = 0
    for i in range(len(calendar["nrc"])):
        ct_nrc_quantity += 2 * (calendar["nrc"][i].count("/"))
        ct_nrc_alternatives += calendar["other_nrc"][i].count("/")
    
    return ct_nrc_quantity*nrc_quantity + ct_nrc_alternatives*nrc_alternatives


def configure():
    print("There are 9 modules")
    print("1: from 08:20 to 09:30")
    print("2: from 09:40 to 10:50")
    print("3: from 11:00 to 12:10")
    print("4: from 12:20 to 13:30")
    print("--Lunch Time--")
    print("5: from 14:00 to 16:00")
    print("6: from 16:10 to 17:20")
    print("7: from 17:30 to 18:40")
    print("8: from 18:50 to 20:00")
    print("9: from 20:10 to 21:20")
    start_time = int(input("on what module you want to start? "))
    end_time = int(input("on what module you want to end? "))
    
    print("Write the days that you would want to go to class (ex. L M W J V S).")
    days = input("days: ").upper()

    print("Do you want free modules in between?")
    fm_days = int(input("How many days? "))
    fm_min = int(input("Minimum free modules: "))
    fm_max = int(input("Maximum free modules: "))
    fm_next = input("next to: ")

    nrc_quantity = 0
    if input("Do you want to consider nrc quantity to the point system (y/n)?").lower() == "y":
        nrc_quantity = 1

    nrc_alternatives = 0
    if input("Do you want to consider nrc alternatives to the point system (y/n)?").lower() == "y":
        nrc_alternatives = 1

    data = {
        "start_time": start_time,
        "end_time": end_time,
        "days": days,
        "weight_in_preferred_hours":4,
        "weight_in_preferred_days":6,
        "free_module": {
            "quantity_days": fm_days,
            "min_hours":fm_min,
            "max_hours":fm_max,
            "next_to": fm_next,
            "weight":2
        },
        "nrc":{
            "nrc_quantity_weight": nrc_quantity,
            "nrc_alternatives_weight":nrc_alternatives
        }
    }
    json_writer(path_file="config.json", data=data)