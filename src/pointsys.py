from parsing import *
EXAMPLE = {'calendar': ['LAB/L:5-6 CLAS/M-J:1', 'CLAS/M-J:2', 'CLAS/L-W-V:2 AYU/M-J:4', 'CLAS/L-W:1 AYU/V:1', 'CLAS/L-W:3 AYU/J:6 TAL/V:3', 'LAB/M:5'], 'name': ['Programación', 'Teología', 'Cálculo II', 'Economía', 'Dinámica', 'Lab Dinámica']}

EXAMPLE2 = {'calendar': ['LAB/L:5-6 CLAS/M-J:1', 'CLAS/M-J:4', 'CLAS/L-W-J:3 LAB/M:6 AYU/V:1', 'CLAS/M-J:2 AYU/W:6', 'CLAS/L-W:4 AYU/J:6 TAL/V:4', 'LAB/V:5'], 'name': ['Programación', 'Teología', 'Cálculo II', 'Economía', 'Dinámica', 'Lab Dinámica']}

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
                pnt = 0
                if (a <= i): 
                    pnt = abs(i-a) 
                else: 
                    pnt = abs(i-b)
                points -= pnt
    return points
                
def classes_in_days(calendar, days):
    points = 0
    for i in range(9):
        for j in range(6):
            s = what_is(get_day(j),i,calendar)
            if s != "" and not(get_day(j) in days):
                points -= 5
    return points

def free_modules(calendar, fm_days, fm_min, fm_max, fm_next):
    days = 0
    points = 0
    for j in range(6):
        len = 0
        this_day = False
        for k in range(9):
            i = k+1
            if what_is(get_day(j),i,calendar) == "":
                len += 1
                this_day = True
            else:
                points -= len
                len = 0
        if this_day:
            days +=1
    
    points -= 2 * abs(fm_days-days)

            
    return points


'''
calendar_show(EXAMPLE)
print(classes_in_between_hours(EXAMPLE, 1, 4))
print(classes_in_days(EXAMPLE, 'L M W'))
print(free_modules(EXAMPLE, 2, 1, 1, "Programación"))


calendar_show(EXAMPLE2)
print(classes_in_between_hours(EXAMPLE2, 1, 4))
print(classes_in_days(EXAMPLE2, 'L M W'))
print(free_modules(EXAMPLE2, 2, 1, 2, "Programación"))

'''