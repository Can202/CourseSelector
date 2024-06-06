# Constants
ROW_SKIP = 1
COLUMN_SKIP = 1

from func import *
from parsing import *
from algorithm import *

def main():
    while True:
        option_selected = menu1()
        if option_selected == "0":
            break
        if option_selected == "1":
            start()
        if option_selected == "2":
            create_template()
        if option_selected == "3":
            configure()

def menu1():
    print("What do you want to do?")
    print("[1] Read and analyze the data")
    print("[2] Create template")
    print("[3] Configure")
    print("[0] Exit")
    return input("Select: ")

def menu2():
    print("What do you want to do?")
    print("[1] Show all calendars")
    print("[2] Show best 5")
    print("[3] Show best 10")
    print("[0] Exit")
    return input("Select: ")

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
    a = int(input("on what module you want to start? "))
    b = int(input("on what module you want to end? "))
    
    print("Write the days that you would want to go to class (ex. L M W J V S).")
    days = input("days: ").upper()

    print("Do you want free modules in between?")
    fm_days = int(input("How many days? "))
    fm_min = int(input("Minimum free modules: "))
    fm_max = int(input("Maximum free modules: "))
    fm_next = input("next to: ")



def start():
    data = get_data()

    # Doing the algorithm
    options = get_valid_options(data)

def create_template():
    pass

if __name__ == "__main__":
    main()