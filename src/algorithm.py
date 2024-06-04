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
    a = the_loop(data, courses_id, courses_options, 0)
    print(a)

def the_loop(data, id, options, number, the_list = {"calendar": [], "name": []}):
    if number >= len(id):
        return the_list
    i = id[number]
    print(f"{i}: ---{data[i][0]}---")

    if number != 0:
        for temp_k in range(len(options) - COLUMN_SKIP):
            k = temp_k + COLUMN_SKIP
            val = 0
            val = available(data, i, k, the_list)
            if val != -1:
                val2 = False
                for j in range(len(the_list["calendar"])):
                    if val2 == False:
                        if courses_conflict(text1=the_list["calendar"][j], text2=data[i][k]):
                            val2=True
                            print(f"conflict found between {data[i][0]} {k}", data[i][k],"y", the_list["calendar"][j])

                if val2 == False:
                    print(f"Selected {data[i][0]} {k}", data[i][k])
                    the_list["name"].append(data[i][0])
                    the_list["calendar"].append(data[i][k])
    else:
        the_list["name"].append(data[i][0])
        the_list["calendar"].append(data[i][1])
    
    
    the_list = the_loop(data, id, options, number + 1, the_list)
    return the_list

def available(data, i, k, the_list):
    if data[i][k] == "":
        return -1
    if data[i][0] in the_list["name"]:
        return -1
    return 0


def count_options(row_data):
    count = 0
    for temp in range(len(row_data) - COLUMN_SKIP):
        i = temp + COLUMN_SKIP
        if row_data[i] != "":
            count += 1
    return count
