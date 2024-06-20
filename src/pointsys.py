from parsing import *

def point_system(the_calendars):
    points = [0] * len(the_calendars)

    data = json_reader(path_file="config.json")

    start_time=data["start_time"]
    end_time=data["end_time"]
    days=data["days"]
    
    free_module_quantity_days = data["free_module"]["quantity_days"]
    free_module_min_hours = data["free_module"]["min_hours"]
    free_module_max_hours = data["free_module"]["max_hours"]
    free_module_next_to = data["free_module"]["next_to"]

    for i in range(len(the_calendars)):
        points[i] += classes_in_between_hours(the_calendars[i], start_time, end_time)
        points[i] += classes_in_days(the_calendars[i], days)
        points[i] += free_modules(the_calendars[i], free_module_quantity_days, free_module_min_hours, free_module_max_hours, free_module_next_to)

    return points

def classes_in_between_hours(calendar, a, b):
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
    return points
                
def classes_in_days(calendar, days):
    points = 0
    for i in range(9):
        for j in range(6):
            s = what_is(get_day(j),i,calendar)
            if s != "" and not(get_day(j) in days):
                points -= 5
    return points

def free_modules(calendar, fm_days, fm_min, fm_max, fm_next):
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

            
    return points

