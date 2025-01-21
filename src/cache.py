from func import *
import os
import shutil

MAX_CACHE = 5

def save_cache(main_data, calendars,points):
    calendar_data = {
        "calendars": calendars,
        "main_data":main_data,
        "points":points
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