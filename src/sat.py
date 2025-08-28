from ortools.sat.python import cp_model
from func import *
import parsing


def get_sat_solutions(main_data):
    model = cp_model.CpModel()
    variables = {}
    # Config needed

    if main_data[-1] == ['']:
        main_data = remove_by_index(main_data, -1)

    courses_quantity = len(main_data)
    nrc_quantity = [len(course) - 1 for course in main_data]

    # La idea es hacer esta info variable
    total_days = 6
    total_modules = 9

    # Creating Variables

    for i in range(courses_quantity):
        for j in range(1, nrc_quantity[i] + 1):
            variables[f"{main_data[i][0]}_SEC_{j}"] = model.NewBoolVar(f"{main_data[i][0]}_SEC_{j}")

    for i in range(courses_quantity):
        for j in range(1, total_days + 1):
            for k in range(1, total_modules + 1):
                variables[f"{main_data[i][0]}_D{j}_M{k}"] = model.NewBoolVar(f"{main_data[i][0]}_D{j}_M{k}")

    nrc_by_course, courses_id = main_data_to_days_and_modules(main_data, model, variables, total_days, total_modules)
    # leer data para llevar cada nrc a sus cursos como más variables
    # poner condiciones (único nrc por curso) implicancia de bloques de cada nrc, restricción tope
    # resolver, guardar soluciones en objetos de clases calendar/nrc/block ?
    # test
    print(model)
    return nrc_by_course, courses_id


def main_data_to_days_and_modules(main_data, bool_sat_model, variables_dict, total_days=6, total_modules=9):
    nrc_by_course = []
    courses_id = []
    for course in main_data:
        nrc_this_course = []
        i = 1
        courses_id.append(course[0])
        course.pop(0)
        for nrc in course:
            nrc_data = nrc.split(" ")

            nrc_id = nrc_data[0][1:]
            nrc_this_course.append(nrc_id)

            # Cleaning nrc_data to only show courses.
            nrc_data.pop(0)
            cleaning_prof = True
            while cleaning_prof:
                if ":" in nrc_data[-1]:
                    cleaning_prof = False
                else:
                    nrc_data.pop(-1)

            nrc_data = " ".join(nrc_data)
            print(nrc_data)

            modules_used_array = parsing.get_schedule_number_array(nrc_data)
            #used_vars = []

            #for block in nrc_data:
            #    if block[0] == "$":
            #        # Saving nrcs list for the future.
            #        nrc_this_course.append(block[1:])
            #    elif "(" in block or ")" in block:
            #        pass
            #    else:
            #        index = block.find("/")
            #        block_cut = block[index + 1:]
            #        index = block_cut.find(":")
            #        num = block_cut[index + 1:]
            #        days = block_cut[:index]
            #
            #        if "-" in days:
            #            days = days.split("-")
            #            for day in days:
            #                day = day_to_numeric(day)
            #                bool_sat_model.AddImplication(variables_dict[f"{courses_id[i-1]}_SEC_{i}"],
            #                                              variables_dict[f"{courses_id[i-1]}_D{day}_M{num}"])
            #                used_vars.append([day, num])
            #        else:
            #            day = day_to_numeric(days)
            #            bool_sat_model.AddImplication(variables_dict[f"{courses_id[i-1]}_SEC_{i}"],
            #                                          variables_dict[f"{courses_id[i-1]}_D{day}_M{num}"])
            #            used_vars.append([day, num])

            # Make negative any other DX_MY
            for j in range(1, total_days + 1):
                for k in range(1, total_modules + 1):
                    if modules_used_array[i-1, j-1] == 0:
                        bool_sat_model.AddImplication(variables_dict[f"{courses_id[i-1]}_SEC_{i}"],
                                                      variables_dict[f"{courses_id[i-1]}_D{j}_M{k}"].Not())
                    else:
                        bool_sat_model.AddImplication(variables_dict[f"{courses_id[i - 1]}_SEC_{i}"],
                                                      variables_dict[f"{courses_id[i - 1]}_D{j}_M{k}"])
        i += 1
        nrc_by_course.append(nrc_this_course)
    return nrc_by_course, courses_id


def day_to_numeric(day):
    if day == "L":
        return 1
    elif day == "M":
        return 2
    elif day == "W":
        return 3
    elif day == "J":
        return 4
    elif day == "V":
        return 5
    else:
        return -1
