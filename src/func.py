
import json
import requests
DEBUG = False

# Here will be functions to make some specific functionality

def save_file(*, path,text):
    file = open(path, "w", encoding="utf-8")
    file.write(text)
    file.close()

def csv_reader(*, path_file = ""):
    file = open(path_file, "r", encoding="utf-8")
    data = file.read()
    file.close()
    return data

def json_reader(*, path_file = ""):
    with open(path_file, 'r') as file:
        return json.load(file)

def json_writer(*, path_file = "", data):
    with open(path_file, 'w') as file:
        json.dump(data, file, indent=4)

# get data (array) from the raw data (str)
def get_data_from_raw_data(*, raw_data = ""):
    raw_data_lines = raw_data.split("\n")
    data = []
    for i in range(len(raw_data_lines)):
        data.append(raw_data_lines[i].split(","))
    return data

# Takes one list as a principal list, then sorts every list in others (list of list) and the principal list, by ascending order of the principal list 
def sort_many_lists_by_ascending_order_of_one_list(principal, others):
    n = len(principal)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if principal[j] > principal[j+1]:
                principal[j], principal[j+1] = principal[j+1], principal[j]
                for k in range(len(others)):
                    others[k][j], others[k][j+1] = others[k][j+1], others[k][j]
                swapped = True
        if not swapped:
            break
    return [principal, others]


# Takes one list as a principal list, then sorts every list in others (list of list) and the principal list, by descending order of the principal list 
def sort_many_lists_by_descending_order_of_one_list(principal, others):
    n = len(principal)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if principal[j] < principal[j+1]:
                principal[j], principal[j+1] = principal[j+1], principal[j]
                for k in range(len(others)):
                    others[k][j], others[k][j+1] = others[k][j+1], others[k][j]
                swapped = True
        if not swapped:
            break
    return [principal, others]

def multiplication_of_each_element(some_list):
    multiplication = 1
    for element in some_list:
        multiplication *= element
    return multiplication

# Remove an element of a list by index
def remove_by_index(lst, index):
    if -len(lst) <= index < len(lst):
        del lst[index]
    return lst

# Debug function, used to print information if DEBUG constant is set True.
def Debug(text, *, debug_mode = True,ignore_debug_statement=False):
    if debug_mode:
        if DEBUG or ignore_debug_statement:
            print(text)
    else:
        if (not DEBUG) or ignore_debug_statement:
            print(text, end="")


# This function is used to display a loading animation.
# You have to put it in a for loop, giving the total length and i variable,
# If the part has a lot of for loops, you can create Parts, the function will divide the percentages
# for each part.
def loadingAnimation(*,part=1, i=0, n=100, done=False, maxPart = 4):
    percentageperPart = 100//maxPart
    if done:
        Debug(f"Loaded [{'-' * 100}] 100%  \n", debug_mode=False)
        return
    #Update percentaje
    percentage = percentageperPart * (part - 1)
    ppp = percentageperPart / n
    d = (len(str(n))-2)
    if d < 0:
        d=0

    if i%(10**d) == 0:
        percentage += ppp * i
        p = int(percentage)
        Debug(f"(p.{part:02}) [{'-' * (p-1)}{'/'}{' ' * (100-p)}] {p}%    ""\r", debug_mode=False)

# Input integer manager, with error messages and repetition
def input_integer(*,text="",min=1, max=2):
    while True:
        try:
            user_input = input(text).strip()
            number = int(user_input)
            
            if min <= number <= max:
                return number
            else:
                print(f"Error: Enter a number between {min} and {max}.")
        except ValueError:
            print("Error: Please enter a valid integer.")

# Input days manager, with error messages and repetition
def input_days(text=""):
    valid_days = {"L", "M", "W", "J", "V", "S"}
    while True:
        user_input = input(text).upper().strip()
        days = user_input.split()
        
        if all(day in valid_days for day in days):
            return days
        else:
            print("Error: Please enter valid days using abbreviations (e.g., L M W J V S).")

def check_website_connection(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        # Check if the response code indicates success (200-299)
        if 200 <= response.status_code < 300:
            return True
        else:
            return False
    except requests.RequestException as e:
        return False