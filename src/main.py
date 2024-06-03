
def main():
    data = get_data()
    while True:
        option_selected = menu()
        if option_selected == "0":
            break
        if option_selected == "1":
            start()
        if option_selected == "2":
            create_template()


def csv_reader(*, path_file = ""):
    file = open(path_file, "r", encoding="utf-8")
    data = file.read()
    file.close()
    return data

def plain_text_to_array(*, data = ""):
    data_lines = data.split("\n")
    data_splitted = []
    for i in range(len(data_lines)):
        data_splitted.append(data_lines[i].split(","))
    return data_splitted

def get_data():
    raw_data = csv_reader(path_file="data.csv")
    return plain_text_to_array(data=raw_data)

def menu():
    print("What do you want to do?")
    print("[1] Read and analyze the data")
    print("[2] Create template")
    print("[0] Exit")
    return input("Select: ")

def start():
    pass
def create_template():
    pass

if __name__ == "__main__":
    main()