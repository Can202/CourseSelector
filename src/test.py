import func
import parsing
import sat

def csv_reader(*, path_file=""):
    file = open(path_file, "r", encoding="utf-8")
    data = file.read()
    file.close()
    return data


def plain_text_to_array(*, data=""):
    data_lines = data.split("\n")
    data_splitted = []
    for i in range(len(data_lines)):
        data_splitted.append(data_lines[i].split(","))
    return data_splitted


#data1 = csv_reader(path_file="data.csv")
#data_array = plain_text_to_array(data=data1)  # there exist empty elements at the end of list
#print(data_array)

# get data from raw data convierte texto a lista doble separada por comas (csv)
lista_test = parsing.get_main_data()
# print(lista_test)
a = sat.get_sat_solutions(lista_test)
print(a.SolutionCount())
print(sat.get_nrc_info())

#number_array = parsing.get_schedule_number_array("AYU/L:6 CLAS/M-J:2 LAB/W:6")
#print(number_array)
