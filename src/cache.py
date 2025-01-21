from func import *
import os
import shutil
import main

MAX_CACHE = 20

def get_date_and_list_of_courses():
    raw_main_data = csv_reader(path_file="data.csv")
    raw_main_data = raw_main_data[:find_kth_occurrence("\n", raw_main_data, 1)]
    for d in raw_main_data.split(","):
        if "!" in d:
            date = d[find_kth_occurrence("!", d, 1)+1:]
        if "#" in d:
            courses = d[find_kth_occurrence("#", d, 1)+1:]
        if "&" in d:
            semester = d[find_kth_occurrence("&", d, 1)+1:]
    return date, courses, semester

def save_cache(main_data, calendars,points):
    if MAX_CACHE == 0:
        return
    main_raw_data = csv_reader(path_file="data.csv")
    date, courses, semester = get_date_and_list_of_courses()
    calendar_data = {
        "calendars": calendars,
        "main_data":main_data,
        "main_raw_data":main_raw_data,
        "points":points,
        "date":date,
        "courses":courses,
        "semester":semester
    }
    for i in range(0,MAX_CACHE):
        t = MAX_CACHE-i
        rename_caches(t)
    json_writer(path_file="cache/1",data=calendar_data)

def rename_caches(number=1):
    if not os.path.exists(f"cache/{number}"):
        return
    if number == MAX_CACHE:
        os.remove(f"cache/{number}")
    else:
        os.rename(f"cache/{number}",f"cache/{number+1}")

def in_cache(main_data):
    if MAX_CACHE == 0:
        return 0
    for i in range(MAX_CACHE):
        if in_cache_from_number(main_data, number=i):
            return i
        
    return 0

def in_cache_from_number(main_data, number=1):
    if not os.path.isfile(f"cache/{number}"):
        return False

    calendar_data = json_reader(path_file=f"cache/{number}")
    if calendar_data["main_data"] == main_data:
        return True
    return False

def load_cache(number=1):
    calendar_data = json_reader(path_file=f"cache/{number}")
    return calendar_data["calendars"], calendar_data["points"]

def save_csv_cache(number=1):
    calendar_data = json_reader(path_file=f"cache/{number}")
    save_file(path="data.csv", text=calendar_data["main_raw_data"])

def load_cache_info(number=1):
    
    if not os.path.isfile(f"cache/{number}"):
        return "", "", ""
    calendar_data = json_reader(path_file=f"cache/{number}")
    return calendar_data["courses"], calendar_data["date"], calendar_data["semester"]

def clear():
    path = "cache"
    if not os.path.exists(path):
        raise FileNotFoundError(f"The folder '{path}' does not exist.")
    
    if not os.path.isdir(path):
        raise NotADirectoryError(f"The path '{path}' is not a folder.")
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)