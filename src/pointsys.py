from parsing import *
import shutil

# Main functions, returns a point list where the index matches the calendar index in calendars list
def point_system(calendars,progress_callback=None):
    points = [100] * len(calendars)

    config_data = json_reader(path_file="config.json")

    start_time=config_data["start_time"]
    end_time=config_data["end_time"]
    days=config_data["days"]
    hours_weight=config_data["weight_in_preferred_hours"]
    days_weight=config_data["weight_in_preferred_days"]
    
    free_module_quantity_days = config_data["free_module"]["quantity_days"]
    free_module_min_hours = config_data["free_module"]["min_hours"]
    free_module_max_hours = config_data["free_module"]["max_hours"]
    free_module_next_to = config_data["free_module"]["next_to"]
    free_module_weight = config_data["free_module"]["weight"]

    nrc_quantity= config_data["nrc"]["nrc_quantity_weight"]
    nrc_alternatives= config_data["nrc"]["nrc_alternatives_weight"]


    for i in range(len(calendars)):
        loadingAnimation(part=6, i=i, n=len(calendars),progress_callback=progress_callback)
        points[i] += classes_in_between_hours(calendars[i], start_time, end_time, hours_weight)
        points[i] += classes_in_days(calendars[i], days, days_weight)
        points[i] += free_modules(calendars[i], free_module_quantity_days, free_module_min_hours, free_module_max_hours, free_module_next_to, free_module_weight)
        points[i] += fn_nrc_quantity(calendars[i], nrc_quantity,nrc_alternatives)

    return points


def classes_in_between_hours(calendar, a, b, weight):
    points = 0
    for i in range(9):
        for j in range(6):
            s = get_section_class_on_time(calendar=calendar, day = get_day(j), hour = i)
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
            s = get_section_class_on_time(calendar=calendar, day = get_day(j), hour = i)
            if s != "" and not(get_day(j) in days):
                points -= 1
    return points * weight

# Not working right yet
def free_modules(calendar, fm_days, fm_min, fm_max, fm_next, free_module_weight):
    days = 0
    points = 0
    for j in range(6):
        len = 0
        this_day = False
        for k in range(9):
            i = k+1
            if get_section_class_on_time(calendar=calendar, day = get_day(j), hour = i) == "":
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
    for i in range(len(calendar["sections_nrc_bundle"])):
        ct_nrc_quantity += 2 * (calendar["sections_nrc_bundle"][i].count("/"))
        ct_nrc_alternatives += calendar["sections_nrc_alternative_bundle"][i].count("/")
    
    return ct_nrc_quantity*nrc_quantity + ct_nrc_alternatives*nrc_alternatives


def reset_config():
    shutil.copyfile("default/config","config.json")
    shutil.copyfile("default/professors_banned","professors_banned.txt")
    shutil.copyfile("default/professors_featured","professors_featured.txt")