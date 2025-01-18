import pointsys
import parsing
import algorithm
import automatic
# Testing that everything works

# Point system
EXAMPLE = {'calendar': ['LAB/L:5-6 CLAS/M-J:1', 'CLAS/M-J:2', 'CLAS/L-W-V:2 AYU/M-J:4', 'CLAS/L-W:1 AYU/V:1', 'CLAS/L-W:3 AYU/J:6 TAL/V:3', 'LAB/M:5'], 'name': ['Programación', 'Teología', 'Cálculo II', 'Economía', 'Dinámica', 'Lab Dinámica']}
EXAMPLE2 = {'calendar': ['LAB/L:5-6 CLAS/M-J:1', 'CLAS/M-J:4', 'CLAS/L-W-J:3 LAB/M:6 AYU/V:1', 'CLAS/M-J:2 AYU/W:6', 'CLAS/L-W:4 AYU/J:6 TAL/V:4', 'LAB/V:5'], 'name': ['Programación', 'Teología', 'Cálculo II', 'Economía', 'Dinámica', 'Lab Dinámica']}
a=pointsys.classes_in_between_hours(EXAMPLE, 1, 4) == -18
a=a and pointsys.classes_in_days(EXAMPLE, 'L M W') == -35
a=a and pointsys.free_modules(EXAMPLE, 2, 1, 1, "Programación") == -12
a=a and pointsys.classes_in_between_hours(EXAMPLE2, 1, 4) == -28
a=a and pointsys.classes_in_days(EXAMPLE2, 'L M W') == -40
a=a and pointsys.free_modules(EXAMPLE2, 2, 1, 2, "Programación") == -18
if a:
    print("Point system working")
else:
    print("Point system NOT working")



# Function new
data=[['Cálculo II', 'CLAS/L-W-V:2 AYU/M-J:4', 'CLAS/L-W-V:4 LAB/W:1 AYU/J:4', 'CLAS/L-W-J:3 LAB/M:6 AYU/V:1', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['Programación', 'LAB/L:5-6 CLAS/M-J:1', 'CLAS/L-W:3 LAB/L:5-6', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['Economía', 'CLAS/M-J:2 AYU/W:6', 'CLAS/L-W:1 AYU/V:1', 'CLAS/L-W:1 AYU/V:1', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['Teología', 'CLAS/M-J:2', 'CLAS/M-J:4', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['Dinámica', 'CLAS/L-W:2 AYU/J:6 TAL/V:2', 'CLAS/L-W:3 AYU/J:6 TAL/V:3', 'CLAS/L-W:4 AYU/J:6 TAL/V:4', 'CLAS/L-W:4 AYU/L:5 TAL/V:4 ', 'CLAS/L-W:3 AYU/L:5 TAL/V:3', 'CLAS/L-W:2 AYU/J:6 TAL/V:2', '', '', '', '', '', '', '', '', '', ''], ['Lab Dinámica', 'LAB/M:5', 'LAB/W:5', 'LAB/J:5', 'LAB/V:5', 'LAB/M:4', 'LAB/J:4', 'LAB/L:6', 'LAB/M:6', 'LAB/W:6', 'LAB/M:2', 'LAB/J:2', 'LAB/L:4', 'LAB/W:4', 'LAB/L:1', 'LAB/V:4', 'LAB/W:1'], ['']]
courses_id=[1, 3, 0, 2, 4, 5]
courses_options=[2, 2, 3, 3, 6, 16]
print(algorithm.raw_list_of_all_calendars(data, courses_id, courses_options))



print("----------")
print(parsing.get_days_array("CLAS/L-W-V:2 AYU/M-J:4") == parsing.get_days_array("CLAS/L-W:2 CLAS/V:2 AYU/M-J:4"))
print(parsing.get_days_array_np("CLAS/L-W:2 CLAS/V:2 AYU/M-J:4"))



# Automatic.py
print("FIS0152",automatic.formatting_get_courses(Semestre="2025-1",Sigla="FIS0152"))