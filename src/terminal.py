# Constants
ROW_SKIP = 1
COLUMN_SKIP = 1

import shutil
# My code
from func import *
import parsing
import algorithm
import pointsys
import automatic
import cache

# Main function
def run_terminal():
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
            menu_automatic()
        if option_selected == 5:
            cache.clear()
            print("Cache cleared")
        if option_selected == 6:
            load_custom_cache_menu()

# Menu #1 display
def menu1():
    print("What do you want to do?")
    print("[1] Read and analyze the data")
    print("[2] Reset default")
    print("[3] Configure")
    print("[4] Create csv file")
    print("[5] Clear cache")
    print("[6] Load from your cache")
    print("[0] Exit")
    return input_integer(text="Select: ", min=0, max=45)

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
def start(calendars=[], points=[]):
    create_folder("cache")
    if not os.path.isfile("data.csv"):
        print("There is not data.csv file")
        return 

    main_data = parsing.get_main_data()

    # Doing the algorithm
    if len(calendars) == 0:
        calendars, points, cache_used = algorithm.get_calendars_from_data(main_data)

    if len(calendars) == 0:
        print("There's not calendars without conflicts.")
        return
    
    NRC_on = calendars[0]["nrc_active"]

    
    while True:
        ans = menu2(NRC_on)
        if ans == 0:
            break
        if ans == 1:
            show_n_calendars(calendars, points)
        if ans == 2:
            show_n_calendars(calendars, points,3)
        if ans == 3:
            show_n_calendars(calendars, points,5)
        if ans == 4:
            show_n_calendars(calendars, points,10)
        if ans == 5:
            n = input_integer(text="How many? ",min=1, max=len(calendars))
            show_n_calendars(calendars, points,n)
        if ans == 6 and NRC_on:
            show_nth_calendar_with_NRC_information(calendars, points)

def show_nth_calendar_with_NRC_information(calendars, points):
    n = int(input("Number of the calendar: ")) - 1
    print(f"---Calendar {n+1}---")
    parsing.calendar_show(calendars[n])
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
        parsing.calendar_show(calendars[i])


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

def load_custom_cache_menu():
    print("Your cache:")
    max = cache.MAX_CACHE
    doing_max = True
    happen = False
    for i in range(1,cache.MAX_CACHE+1):
        courses, date, semester = cache.load_cache_info(number=i)
        if date != "":
            print(f"[{i}] ({date}): {semester} / {courses}")
            happen = True
        else:
            if doing_max:
                max = i
                doing_max = False
    if happen == False:
        max = -1
    else:
        print("[0] None")
    loading = input_integer(text="Which cache do you want to load? ", min=0,max=max)
    if loading == -1:
        print("There is no cache.")
        return
    if loading == 0:
        return
    cache.save_csv_cache(number=loading)
    calendars, points = cache.load_cache(number=loading)
    start(calendars=calendars, points=points)

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
    start_time = input_integer(text="on what module you want to start? ", min=1, max=9)
    end_time = input_integer(text="on what module you want to end? ", min=start_time, max=9)

    hours_weight = input_integer(text="How much weight do you want to be considered on the hours of your classes? ", min=0, max=10)
    
    print("Write the days that you would want to go to class (e.g. L M W J V S)")
    days = input_days("days: ")
    
    days_weight = input_integer(text="How much weight do you want to be considered on the days of your classes? ", min=0, max=10)
    

    print("Do you want free modules in between?")
    fm_days = input_integer(text="How many days? ", min=0, max=6)
    fm_min = input_integer(text="Minimum free modules: ", min=0, max=9)
    fm_max = input_integer(text="Maximum free modules: ", min=fm_min, max=9)
    fm_next = input("next to: ")
    fm_weight = input_integer(text="How much weight do you want to be considered on the free modules of your schedule? ", min=0, max=10)


    nrc_quantity = input_integer(text="How much weight do you want to be considered on the quantity of nrc? ", min=0, max=10)
    nrc_alternatives = input_integer(text="How much weight do you want to be considered on the quantity of nrc alternatives? ", min=0, max=10)

    config_data = {
        "start_time": start_time,
        "end_time": end_time,
        "days": days,
        "weight_in_preferred_hours":hours_weight,
        "weight_in_preferred_days":days_weight,
        "free_module": {
            "quantity_days": fm_days,
            "min_hours":fm_min,
            "max_hours":fm_max,
            "next_to": fm_next,
            "weight":fm_weight
        },
        "nrc":{
            "nrc_quantity_weight": nrc_quantity,
            "nrc_alternatives_weight":nrc_alternatives
        }
    }
    json_writer(path_file="config.json", data=config_data)

def menu_automatic():

    if not check_website_connection("https://buscacursos.uc.cl"):
        print("No connection to BuscaCursos.")
        print("Check your connection to the internet or check if the BuscaCursos web is working")
        return -1

    print("----- EXAMPLE -----")
    print("Semester: 2025-1")
    print("Courses to look: MAT1630 MAT1640 FIS0152 FIS1523 OPT-FIL2005/VET161G IMT1001")
    print("----- EXAMPLE -----")
    semestre = input("Semester: ")
    courses = input("Courses to look: ")
    course = courses.split(" ")
    automatic.create_csv_from_list(Semestre=semestre, courses_id_bundle=course)
    print("Done!")
    print("Review the csv file! To check if everything is right.")

if __name__=="__main__":
    run_terminal()