from ortools.sat.python import cp_model
from func import *
import parsing
from classes import *


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

    courses_id, blabla = get_courses_id()
    main_data_to_days_and_modules(model, variables, total_days, total_modules)
    one_ncr_course_constraint(model, variables)
    at_most_one_module(bool_sat_model=model, variables_dict=variables, courses_id=courses_id,
                       total_days=total_days, total_modules=total_modules)

    solver = cp_model.CpSolver()
    result = solver.Solve(model)

    if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Solución encontrada:")
        for var_name, var in variables.items():
            if solver.Value(var) == 1:
                print(var_name, "= 1")
    elif result == cp_model.INFEASIBLE:
        print("a bueno cagaste")
    else:
        print("No hay solución :(")
        print(result)
    # resolver, guardar soluciones en objetos de clases calendar/nrc/block ?

    solver = cp_model.CpSolver()
    solution_printer = AllSolutionsPrinter(variables)
    status = solver.SearchForAllSolutions(model, solution_printer)
    return solution_printer


def main_data_to_days_and_modules(bool_sat_model, variables_dict, total_days=6, total_modules=9):

    courses_id, main_data = get_courses_id()
    nrc_by_course = get_nrc_info()
    for course_num in range(len(courses_id)):
        for i in range(1, len(nrc_by_course[course_num])+1):
            nrc_data = get_nrc_info(is_nrc_data=True, course_pos=course_num, nrc_pos=i-1)
            modules_used_array = parsing.get_schedule_number_array(nrc_data)
            # Creating constraints
            for j in range(total_days):
                for k in range(total_modules):
                    if modules_used_array[k, j] == 0:
                        bool_sat_model.AddImplication(variables_dict[f"{courses_id[course_num]}_SEC_{i}"],
                                                      variables_dict[f"{courses_id[course_num]}_D{j+1}_M{k+1}"].Not())
                    else:
                        bool_sat_model.AddImplication(variables_dict[f"{courses_id[course_num]}_SEC_{i}"],
                                                      variables_dict[f"{courses_id[course_num]}_D{j+1}_M{k+1}"])
    return courses_id


# Se ha hecho solo un caso, se deben juntar todos en un gran Or.
def one_ncr_course_constraint(bool_sat_model, variables_dict):
    courses_id, main_data = get_courses_id()
    nrc_by_course = get_nrc_info()

    for i in range(len(courses_id)):
        all_constraints = [variables_dict[f"{courses_id[i]}_SEC_{k+1}"] for k in range(len(nrc_by_course[i]))]
        bool_sat_model.AddExactlyOne(all_constraints)


def at_most_one_module(*, bool_sat_model, variables_dict, courses_id, total_days=6, total_modules=9):
    for i in range(total_days):
        for j in range(total_modules):
            block_constraint = [variables_dict[f"{courses_id[k]}_D{i+1}_M{j+1}"] for k in range(len(courses_id))]
            bool_sat_model.AddAtMostOne(block_constraint)


def get_courses_id():
    main_data = parsing.get_main_data()
    courses_id = []
    for course in main_data:
        courses_id.append(course[0])
        course.pop(0)

    return courses_id, main_data


def correct_main_data():
    main_data = parsing.get_main_data()
    for course in main_data:
        course.pop(0)

    return main_data


def get_nrc_info(*, is_nrc_data=False, course_pos=0, nrc_pos=0):
    main_data = correct_main_data()

    if is_nrc_data:
        nrc = main_data[course_pos][nrc_pos]
        nrc_data = nrc.split(" ")

        nrc_data.pop(0)
        cleaning_prof = True
        while cleaning_prof:
            if ":" in nrc_data[-1]:
                cleaning_prof = False
            else:
                nrc_data.pop(-1)
        #print(nrc_data)

        nrc_data = " ".join(nrc_data)
        # Return case 1: data of modules of only one nrc as string
        return nrc_data

    nrc_by_course = []

    for course in main_data:
        nrc_this_course = []
        for nrc in course:
            nrc_data = nrc.split(" ")

            nrc_id = nrc_data[0][1:]
            nrc_this_course.append(nrc_id)

        nrc_by_course.append(nrc_this_course)
    # Return case 2: List of all nrc codes with index [course][section] (is_nrc_data = False)
    return nrc_by_course
