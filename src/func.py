
import json

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

def plain_text_to_array(*, data = ""):
    data_lines = data.split("\n")
    data_splitted = []
    for i in range(len(data_lines)):
        data_splitted.append(data_lines[i].split(","))
    return data_splitted

def many_sorts(principal, others):
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


def many_sorts_MAX(principal, others):
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

def variation(some_list):
    multiplication = 1
    for element in some_list:
        multiplication *= element
    return multiplication

def base_list(list, n):
    level = [0] * len(list)
    for i in range(len(list)):
        j = len(list) - i-1
        level[j] = n % list[j] + 1
        n = n // list[j]
    return level

def base_n(list, alist):
    n = 0
    for i in range(len(list)):
        if i == len(list)-1:
            n += (alist[i] - 1)
        else:
            n += variation(list[i+1:]) * (alist[i] - 1 )
    return n

def Debug(text, ignore_debug_statement=False):
    if DEBUG or ignore_debug_statement:
        print(text)
