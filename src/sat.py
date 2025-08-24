from ortools.sat.python import cp_model
from func import *


def get_sat_solutions(main_data):
    model = cp_model.CpModel()
    # Config needed

    if main_data[-1] == ['']:
        main_data = remove_by_index(main_data, -1)

    courses_quantity = len(main_data)
    nrc_quantity = [len(course)-1 for course in main_data]

    # Creating Variables

    for i in range(courses_quantity):
        for j in range(1, nrc_quantity[i]+1):
            model.NewBoolVar(f"{main_data[i][0]}_NRC_{j}")
    # leer data para llevar cada nrc a sus cursos como más variables
    # poner condiciones (único nrc por curso) implicancia de bloques de cada nrc, restricción tope
    # resolver, guardar soluciones en objetos de clases calendar/nrc/block ?
    # test
    print(model)

