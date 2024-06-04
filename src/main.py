# Constants
ROW_SKIP = 1
COLUMN_SKIP = 1

from func import *
from parsing import *

def main():
    while True:
        option_selected = menu()
        if option_selected == "0":
            break
        if option_selected == "1":
            start()
        if option_selected == "2":
            create_template()

def menu():
    print("What do you want to do?")
    print("[1] Read and analyze the data")
    print("[2] Create template")
    print("[0] Exit")
    return input("Select: ")

def start():
    data = get_data()

    # Doing the algorithm
    options = get_valid_options(data)

def get_valid_options(data):
    # Options
    courses_quantity = len(data) - ROW_SKIP
    courses_id = []
    courses_options = []
    for temp in range(courses_quantity):
        i = temp + ROW_SKIP
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
    for j in range(len(the_list["calendar"])):
        for temp_k in range(options + COLUMN_SKIP):
            k = temp_k - COLUMN_SKIP
            conflic = courses_conflict(text1=the_list["calendar"][j], text2=data[i][k])
            if conflic == False:
                the_list["name"].append(data[i][0])
                the_list["calendar"].append(data[i][k])
                break
        
    
    the_loop(data, id, options, number + 1, the_list)
    return the_list

def count_options(row_data):
    count = 0
    for temp in range(len(row_data) - COLUMN_SKIP):
        i = temp + COLUMN_SKIP
        if row_data[i] != "":
            count += 1
    return count

def create_template():
    pass

if __name__ == "__main__":
    main()