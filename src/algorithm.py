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
    the_loop(data, courses_id, courses_options, 0)

def the_loop(data, id, options, number, the_list = {"calendar": [], "name": []}):
    if number >= len(id):
        print(the_list)
        return the_list
    i = id[number]
    conflic = False

    if number != 0:
        for temp_k in range(len(options) - COLUMN_SKIP):
            k = temp_k + COLUMN_SKIP
            val = 0
            val = available(data, i, k, the_list)
            if val != -1:
                for j in range(len(the_list["calendar"])):
                    val2 = courses_conflict(text1=the_list["calendar"][j], text2=data[1][k])
                    if val2 == True:
                        print(f"{data[i][0]} conflict found")
                        break

                the_list["name"].append(data[i][0])
                the_list["calendar"].append(data[i][k])
                break

    else:
        the_list["name"].append(data[i][0])
        the_list["calendar"].append(data[i][1])
    
    the_loop(data, id, options, number + 1, the_list)
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
