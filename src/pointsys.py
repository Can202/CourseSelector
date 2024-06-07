from parsing import *
EXAMPLE = {'calendar': ['LAB/L:5-6 CLAS/M-J:1', 'CLAS/M-J:2', 'CLAS/L-W-V:2 AYU/M-J:4', 'CLAS/L-W:1 AYU/V:1', 'CLAS/L-W:3 AYU/J:6 TAL/V:3', 'LAB/M:5'], 'name': ['Programación', 'Teología', 'Cálculo II', 'Economía', 'Dinámica', 'Lab Dinámica']}


def point_system(the_calendars):
    points = [0] * len(the_calendars)

    #Starters
    a=1
    b=4
    days='L M W J V'
    
    fm_days = 2
    fm_min = 1
    fm_max = 2
    fm_next = "Programación"
    #----

    for i in range(len(the_calendars)):
        points[i] += classes_in_between_hours(the_calendars[i], a, b)
        points[i] += classes_in_days(the_calendars[i], days)
        points[i] += free_modules(the_calendars[i], fm_days, fm_min, fm_max, fm_next)

    return points

def classes_in_between_hours(calendar, a, b):
    points = 0
    for i in range(9):
        for j in range(6):
            s = what_is(get_day(j),i,calendar)
            if s != "" and not((a <= i) and (i <= b)):
                points -= 1
    return points
                
def classes_in_days(calendar, days):
    points = 0
    for i in range(9):
        for j in range(6):
            s = what_is(get_day(j),i,calendar)
            if s != "" and not(get_day(j) in days):
                points -= 1
    return points

def free_modules(calendar, fm_days, fm_min, fm_max, fm_next):
    return 0

#calendar_show(EXAMPLE)
#print(classes_in_between_hours(EXAMPLE, 1, 4))
#print(classes_in_days(EXAMPLE, 'L M W'))