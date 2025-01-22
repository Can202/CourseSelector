import pointsys
import parsing
import algorithm
import automatic
# Testing that everything works


# Function new
data=[['Cálculo II', 'CLAS/L-W-V:2 AYU/M-J:4', 'CLAS/L-W-V:4 LAB/W:1 AYU/J:4', 'CLAS/L-W-J:3 LAB/M:6 AYU/V:1', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['Programación', 'LAB/L:5-6 CLAS/M-J:1', 'CLAS/L-W:3 LAB/L:5-6', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['Economía', 'CLAS/M-J:2 AYU/W:6', 'CLAS/L-W:1 AYU/V:1', 'CLAS/L-W:1 AYU/V:1', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['Teología', 'CLAS/M-J:2', 'CLAS/M-J:4', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['Dinámica', 'CLAS/L-W:2 AYU/J:6 TAL/V:2', 'CLAS/L-W:3 AYU/J:6 TAL/V:3', 'CLAS/L-W:4 AYU/J:6 TAL/V:4', 'CLAS/L-W:4 AYU/L:5 TAL/V:4 ', 'CLAS/L-W:3 AYU/L:5 TAL/V:3', 'CLAS/L-W:2 AYU/J:6 TAL/V:2', '', '', '', '', '', '', '', '', '', ''], ['Lab Dinámica', 'LAB/M:5', 'LAB/W:5', 'LAB/J:5', 'LAB/V:5', 'LAB/M:4', 'LAB/J:4', 'LAB/L:6', 'LAB/M:6', 'LAB/W:6', 'LAB/M:2', 'LAB/J:2', 'LAB/L:4', 'LAB/W:4', 'LAB/L:1', 'LAB/V:4', 'LAB/W:1'], ['']]
courses_id=[1, 3, 0, 2, 4, 5]
courses_options=[2, 2, 3, 3, 6, 16]
print(algorithm.raw_list_of_all_calendars(data, courses_id, courses_options))



print("----------")
print(parsing.get_schedule_array("CLAS/L-W-V:2 AYU/M-J:4") == parsing.get_schedule_array("CLAS/L-W:2 CLAS/V:2 AYU/M-J:4"))
print(parsing.get_schedule_number_array("CLAS/L-W:2 CLAS/V:2 AYU/M-J:4"))
print(parsing.get_schedule_array("CLAS/L-W:2 CLAS/V:2 AYU/M-J:4"))



# Automatic.py
print("FIS0152",automatic.get_courses_data(Semestre="2025-1",Sigla="FIS0152"))

print("AAA")
print("AAA")
print("AAA")
print("AAA")
print(parsing.get_section_schedule_dict(section_schedule="CLAS/L-W:2 CLAS/V:2 AYU/M-J:4"))



print(automatic.check_if_only_type_enabled_and_get_type("MAT1630(AYU*CLAS)"))