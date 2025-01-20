from func import *
import os

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