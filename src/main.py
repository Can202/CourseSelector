# Constants
ROW_SKIP = 1
COLUMN_SKIP = 1

from func import *
from parsing import *
from algorithm import *

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

def create_template():
    pass

if __name__ == "__main__":
    main()