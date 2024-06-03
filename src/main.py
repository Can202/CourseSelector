# Constants
ROW_SKIP = 1
COLUMN_SKIP = 2

def main():
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
    data = get_data()

    # Doing the algorithm
    options = get_valid_options(data)

def get_valid_options(data):
    # Options
    courses_quantity = len(data) - ROW_SKIP
    courses_id = []
    courses_options = []
    for temp in range(courses_quantity):
        i = temp + ROW_SKIP
        courses_options.append(count_options(data[i]))
        courses_id.append(i)
    courses_quantity, [courses_id] = many_sorts(courses_options, [courses_id])
    print(courses_id)
    a = parse_course_info(text=data[5][2])
    b = parse_course_info(text=data[6][2])
    print(courses_conflict(dict1=a, dict2=b))
    
def parse_course_info(*,text =""):
    ts = text.split(" ")
    dic = {}
    for i in range(len(ts)):
        tsa = ts[i].split("/")
        dic[f"{i}_type"] = tsa[0]
        daysC = tsa[1].split(":")[0].split("-")
        days = []
        for j in range(len(daysC)):
            days.append(daysC[j])
        dic[f"{i}_days"] = days
        
        hoursC = tsa[1].split(":")[1].split("-")
        hours = []
        for j in range(len(hoursC)):
            hours.append(hoursC[j])
        dic[f"{i}_hours"] = hours
    dic["len"] = len(ts)
    return dic
def courses_conflict(*, dict1, dict2):
    conflit_in_days= False
    conflit_in_hours= False
    for i in range(dict1["len"]):
        for j in range(dict2["len"]):
            for k in range(len(dict1[f"{i}_days"])):
                if dict1[f"{i}_days"][k] in ''.join(map(str, dict2[f"{j}_days"])):
                    conflit_in_days= True
            for k in range(len(dict1[f"{i}_hours"])):
                if dict1[f"{i}_hours"][k] in ''.join(map(str, dict2[f"{j}_hours"])):
                    conflit_in_hours= True
            if conflit_in_days and conflit_in_hours:
                return True
    return False


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

        

def count_options(row_data):
    count = 0
    for temp in range(len(row_data) - COLUMN_SKIP):
        i = temp + COLUMN_SKIP
        if row_data[i] != "":
            count += 1
    return count


def create_template():
    pass

if __name__ == "__main__":
    main()