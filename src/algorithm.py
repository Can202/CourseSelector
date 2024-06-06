# Constants
ROW_SKIP = 0
COLUMN_SKIP = 1
from func import *
from parsing import *


def get_valid_options(data):
    # Options
    courses_quantity = len(data) - 1
    courses_id = []
    courses_options = []
    for i in range(courses_quantity):
        courses_options.append(count_options(data[i]))
        courses_id.append(i)
    courses_quantity, [courses_id] = many_sorts(courses_options, [courses_id])

    all_calendars(data, courses_id, courses_options)

def all_calendars(data, courses_id, courses_options):
    n = variation(courses_options)
    i = 0

    [a, n] = make_calendar(data, courses_id, courses_options, 0, {"calendar": [], "name": []})
    print(a)

def make_calendar(data, id, options, number, the_list = {"calendar": [], "name": []}, cant = [{"number": -1, "option": -1}], n=0):
    if number >= len(id):
        return [the_list, n]
    i = id[number]
    worked = False
    print(f"{i}: ---{data[i][0]}---")
    

    if number != 0:
        for temp_k in range(len(data[i]) - COLUMN_SKIP):
            k = temp_k + COLUMN_SKIP
            val = 0
            val = available(data, i, k, the_list, number, cant)
            if val != -1:
                val2 = False
                for j in range(len(the_list["calendar"])):
                    if val2 == False:
                        if courses_conflict(text1=the_list["calendar"][j], text2=data[i][k]):
                            val2=True
                            print(f"conflict found between {data[i][0]} #{k}", data[i][k],"y",the_list["name"][j], the_list["calendar"][j])

                if val2 == False:
                    print(f"Selected {data[i][0]} #{k}", data[i][k])
                    the_list["name"].append(data[i][0])
                    the_list["calendar"].append(data[i][k])
                    worked = True
    else:
        print(f"Selected {data[i][0]} #{1}", data[i][1])
        the_list["name"].append(data[i][0])
        the_list["calendar"].append(data[i][1])
        worked = True

    if worked == False:
        print(f"{data[i][0]} not selected")
        the_list["name"].append(data[i][0])
        the_list["calendar"].append("###")

    
    
    [the_list, n] = make_calendar(data, id, options, number + 1, the_list)
    return [the_list, n]

def available(data, i, k, the_list, number, cant):
    if data[i][k] == "":
        return -1
    if data[i][0] in the_list["name"]:
        return -1
    for m in range(len(cant)):
        if cant[m]["number"] == number:
            if k <= cant[m]["option"]:
                print(f"{data[i][0]} #{k} already used")
                return -1

    return 0


def count_options(row_data):
    count = 0
    for temp in range(len(row_data) - COLUMN_SKIP):
        i = temp + COLUMN_SKIP
        if row_data[i] != "":
            count += 1
    return count
