# Constants
ROW_SKIP = 1
COLUMN_SKIP = 1

from func import *
from parsing import *
from algorithm import *
from pointsys import *
import shutil
import automatic

# Main function
def main():
    while True:
        option_selected = menu1()
        if option_selected == 0:
            break
        if option_selected == 1:
            start()
        if option_selected == 2:
            reset_default()
        if option_selected == 3:
            configure()
        if option_selected == 4:
            automatic.menu_automatic()

# Menu #1 display
def menu1():
    print("What do you want to do?")
    print("[1] Read and analyze the data")
    print("[2] Reset default")
    print("[3] Configure")
    print("[4] Create csv file")
    print("[0] Exit")
    return input_integer(text="Select: ", min=0, max=4)

# Menu #2 display
def menu2(NRC_on):
    max = 5
    print("What do you want to do?")
    print("[1] Show all calendars")
    print("[2] Show best 3")
    print("[3] Show best 5")
    print("[4] Show best 10")
    print("[5] Show best n")
    if NRC_on:
        print("[6] Print NRC information of n calendar")
        max = 6
    print("[0] Exit")
    return input_integer(text="Select: ", min=0, max=max)



# Function that starts the analysis of the main data
def start():
    main_data = get_main_data()

    # Doing the algorithm
    the_calendars = get_all_calendars(main_data)

    if len(the_calendars) == 0:
        print("There's not calendars without conflicts.")
        return
    
    NRC_on = the_calendars[0]["nrc_active"]

    # Point system
    points = point_system(the_calendars)
    [points, [the_calendars]] = sort_many_lists_by_descending_order_of_one_list(points, [the_calendars])
    
    while True:
        ans = menu2(NRC_on)
        if ans == 0:
            break
        if ans == 1:
            show_n_calendars(the_calendars, points)
        if ans == 2:
            show_n_calendars(the_calendars, points,3)
        if ans == 3:
            show_n_calendars(the_calendars, points,5)
        if ans == 4:
            show_n_calendars(the_calendars, points,10)
        if ans == 5:
            n = input_integer(text="How many? ",min=1, max=len(the_calendars))
            show_n_calendars(the_calendars, points,n)
        if ans == 6 and NRC_on:
            show_nth_calendar_with_NRC_information(the_calendars, points)

def show_nth_calendar_with_NRC_information(calendars, points):
    n = int(input("Number of the calendar: ")) - 1
    print(f"---Calendar {n+1}---")
    calendar_show(calendars[n])
    print(f"score: {points[n]}")
    print("NRCs:")
    
    max_len = 0
    for i in range(len(calendars[n]["courses_id"])):
        if max_len < len(calendars[n]['sections_nrc_bundle'][i]):
            max_len = len(calendars[n]['sections_nrc_bundle'][i])
    for i in range(len(calendars[n]["courses_id"])):
        if calendars[n]['sections_nrc_alternative_bundle'][i] != "":
            print(f"{calendars[n]['courses_id'][i]}: {(calendars[n]['sections_nrc_bundle'][i]).ljust(max_len+2)} ({calendars[n]['sections_nrc_alternative_bundle'][i]})")
        else:
            print(f"{calendars[n]['courses_id'][i]}: {(calendars[n]['sections_nrc_bundle'][i]).ljust(max_len+2)}")

def show_n_calendars(calendars, points, n=0):
    real_len = 0
    if len(calendars) < n:
        real_len = len(calendars)
    else:
        real_len = n
    if n == 0:
        real_len = len(calendars)
    for i in range(real_len):
        print(f"---Calendar {i+1}---")
        print(f"score: {points[i]}")
        calendar_show(calendars[i])


def reset_default():
    code = "Pi is equal to 4. Change my mind."
    print(code)
    sure = input("Write this to confirm:")
    if code != sure:
        print("Not going to reset")
        return 0

    shutil.copyfile("default/data","data.csv")
    shutil.copyfile("default/config","config.json")
    print("Changed")
    return 0


if __name__ == "__main__":
    main()