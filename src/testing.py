import pointsys
import parsing
# Testing that everything works


# Point system
EXAMPLE = {'calendar': ['LAB/L:5-6 CLAS/M-J:1', 'CLAS/M-J:2', 'CLAS/L-W-V:2 AYU/M-J:4', 'CLAS/L-W:1 AYU/V:1', 'CLAS/L-W:3 AYU/J:6 TAL/V:3', 'LAB/M:5'], 'name': ['Programación', 'Teología', 'Cálculo II', 'Economía', 'Dinámica', 'Lab Dinámica']}
EXAMPLE2 = {'calendar': ['LAB/L:5-6 CLAS/M-J:1', 'CLAS/M-J:4', 'CLAS/L-W-J:3 LAB/M:6 AYU/V:1', 'CLAS/M-J:2 AYU/W:6', 'CLAS/L-W:4 AYU/J:6 TAL/V:4', 'LAB/V:5'], 'name': ['Programación', 'Teología', 'Cálculo II', 'Economía', 'Dinámica', 'Lab Dinámica']}


print(pointsys.classes_in_between_hours(EXAMPLE, 1, 4))
print(pointsys.classes_in_days(EXAMPLE, 'L M W'))
print(pointsys.free_modules(EXAMPLE, 2, 1, 1, "Programación"))


print(pointsys.classes_in_between_hours(EXAMPLE2, 1, 4))
print(pointsys.classes_in_days(EXAMPLE2, 'L M W'))
print(pointsys.free_modules(EXAMPLE2, 2, 1, 2, "Programación"))
