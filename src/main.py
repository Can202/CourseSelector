# Constants
ROW_SKIP = 1
COLUMN_SKIP = 1

from func import *
from parsing import *
from algorithm import *
from pointsys import *
import shutil

def main():
    while True:
        option_selected = menu1()
        if option_selected == "0":
            break
        if option_selected == "1":
            start()
        if option_selected == "2":
            reset_default()
        if option_selected == "3":
            configure()

def menu1():
    print("What do you want to do?")
    print("[1] Read and analyze the data")
    print("[2] Reset default")
    print("[3] Configure")
    print("[0] Exit")
    return input("Select: ")

def menu2():
    print("What do you want to do?")
    print("[1] Show all calendars")
    print("[2] Show best 3")
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
    start_time = int(input("on what module you want to start? "))
    end_time = int(input("on what module you want to end? "))
    
    print("Write the days that you would want to go to class (ex. L M W J V S).")
    days = input("days: ").upper()

    print("Do you want free modules in between?")
    fm_days = int(input("How many days? "))
    fm_min = int(input("Minimum free modules: "))
    fm_max = int(input("Maximum free modules: "))
    fm_next = input("next to: ")

    data = {
        "start_time": start_time,
        "end_time": end_time,
        "days": days,
        "free_module": {
            "quantity_days": fm_days,
            "min_hours":fm_min,
            "max_hours":fm_max,
            "next_to": fm_next
        }
    }
    json_writer(path_file="config.json", data=data)



def start():
    data = get_data()

    # Doing the algorithm
    the_calendars = get_all_calendars(data)

    # Point system
    points = point_system(the_calendars)

    [points, [the_calendars]] = many_sorts_MAX(points, [the_calendars])
    
    while True:
        ans = menu2()
        if ans == "0":
            break
        if ans == "1":
            for i in range(len(the_calendars)):
                print(f"---Calendar {i+1}---")
                print(f"score: {points[i]}")
                calendar_show(the_calendars[i])
        if ans == "2":
            ln=0
            if len(the_calendars) < 3:
                ln = len(the_calendars)
            else:
                ln = 3
            for i in range(ln):
                print(f"---Calendar {i+1}---")
                print(f"score: {points[i]}")
                calendar_show(the_calendars[i])
        if ans == "3":
            ln=0
            if len(the_calendars) < 5:
                ln = len(the_calendars)
            else:
                ln = 5
            for i in range(ln):
                print(f"---Calendar {i+1}---")
                print(f"score: {points[i]}")
                calendar_show(the_calendars[i])
        if ans == "4":
            ln=0
            if len(the_calendars) < 5:
                ln = len(the_calendars)
            else:
                ln = 10
            for i in range(ln):
                print(f"---Calendar {i+1}---")
                calendar_show(the_calendars[i])


def reset_default():
    code = "Pi is equal to 4. Change my mind."
    print(code)
    sure = input("Write this to confirm:")
    if code != sure:
        print("Not going to reset")
        return 0

    shutil.copyfile("default/data.csv","data.csv")
    shutil.copyfile("default/config.json","config.json")
    print("Changed")
    return 0


if __name__ == "__main__":
    main()