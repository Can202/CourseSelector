# Constants
ROW_SKIP = 0
COLUMN_SKIP = 1
from func import *
from parsing import *
import time

def get_all_calendars(data):
    # Options
    courses_quantity = len(data) - 1
    courses_id = []
    courses_options = []
    for i in range(courses_quantity):
        courses_options.append(count_options(data[i]))
        courses_id.append(i)
    courses_quantity, [courses_id] = many_sorts(courses_options, [courses_id])

    the_calendars = all_calendars(data, courses_id, courses_options)
    return the_calendars

def all_calendars(data, courses_id, courses_options):
    n = variation(courses_options)
    #n=10
    i = 0
    a=[]
    start_time = time.time()
    while (i < n):
        ab = make_calendar(data, courses_id, courses_options, 0, {"calendar": [], "name": []}, i)
        a.append(ab[0])
        Debug("---NEXT---")
        i += 1
    
    # Remove lists that aren't complete
    aa = [i for i in a if '###' not in i["calendar"]]

    # Remove duplicates
    the_calendars = []
    for i in range(len(aa)):
        add = True
        for j in range(len(the_calendars)):
            if aa[i] == the_calendars[j]:
                add = False
        if add:
            the_calendars.append(aa[i])
    
    Debug("---Calendars---")
    for i in range(len(the_calendars)):
        Debug(f"---Calendar {i+1}---")
        Debug(the_calendars[i])
        if DEBUG:
            calendar_show(the_calendars[i])

    Debug(f"Calendars Calculated: {n}")
    Debug(f"Calendars w/o conflicts: {len(the_calendars)}")
    Debug(f"--- {(time.time() - start_time)} seconds ---", True)
    return the_calendars

def make_calendar(data, id, options, number, the_list = {"calendar": [], "name": []}, n=0, c=0):
    if number >= len(id):
        return [the_list, n+c, c]
    i = id[number]
    worked = False
    cant = create_cant(options, n)

    Debug(f"{i}: ---{data[i][0]}---")    
    if number != 0:
        for temp_k in range(len(data[i]) - COLUMN_SKIP):
            k = temp_k + COLUMN_SKIP
            val = 0
            val = available(data, i, k, the_list, number, cant)
            if val == 0:
                val2 = False
                for j in range(len(the_list["calendar"])):
                    if val2 == False:
                        if courses_conflict(first_schedule_in_str = the_list["calendar"][j], second_schedule_in_str = data[i][k]):
                            val2=True
                            Debug(f"conflict found between {data[i][0]} #{k} {data[i][k]} y {the_list['name'][j]} {the_list['calendar'][j]}")

                if val2 == False:
                    Debug(f"Selected {data[i][0]} #{k} {data[i][k]}")
                    the_list["name"].append(data[i][0])
                    the_list["calendar"].append(data[i][k])
                    worked = True
    else:
        for temp_k in range(len(data[i]) - COLUMN_SKIP):
            k = temp_k + COLUMN_SKIP
            val = available(data, i, k, the_list, number, cant)
            if val==0 and worked == False:
                Debug(f"Selected {data[i][0]} #{k} {data[i][k]}")
                the_list["name"].append(data[i][0])
                the_list["calendar"].append(data[i][k])
                worked = True

    if worked == False:
        Debug(f"{data[i][0]} not selected")
        the_list["name"].append(data[i][0])
        the_list["calendar"].append("###")

    
    
    [the_list, n, c] = make_calendar(data, id, options, number + 1, the_list, n, c)
    return [the_list, n, c]

def available(data, i, k, the_list, number, cant):
    if data[i][k] == "":
        return -1
    if data[i][0] in the_list["name"]:
        return -1
    for m in range(len(cant)):
        if cant[m]["number"] == number:
            if k <= cant[m]["option"]:
                Debug(f"{data[i][0]} #{k} already used")
                return -2

    return 0

def create_cant(options,n):
    opt = base_list(options, n)
    cant = []
    if n == 0:
        cant.append({"number": -1, "option": -1})
    else:
        for i in range(len(opt)):
            cant.append({"number": i, "option": opt[i]-1})
    return cant

def count_options(row_data):
    count = 0
    for temp in range(len(row_data) - COLUMN_SKIP):
        i = temp + COLUMN_SKIP
        if row_data[i] != "":
            count += 1
    return count

