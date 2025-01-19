# Variable Naming Guidelines (VNG)

We have calendars, courses and sections.

## Types of information
### Courses
#### course_id: (str) The id of a course (e.g. "MAT1630" or "FIL2005")
```
course_id = "FIL2005"
```
#### course_id_bundle: (str) The id of courses in a bundle (e.g. "MAT1630" or "OPT-FIL2005/VET161G")
```
course_id_bundle = "OPT-FIL2005/VET161G"
```
#### course_bundle_id: (str) The id of a bundle of courses (e.g. "MAT1630" or "OPT")
```
course_bundle_id = "OPT"
```

### Sections
#### section_id
```
section_id = "FIL2005"
```
#### section_nrc
```
section_nrc = 14843
```
#### section_nrc_bundle
```
section_nrc_bundle = "14843/14863"
```
#### section_nrc_alternative_bundle
```
section_nrc_alternative_bundle = "14848/14868/14841"
```
#### section_schedule
```
section_schedule = "CLAS/L-M:2-3 AYU/W:2"
```
#### section_schedule_dict: Saves in a dict the schedule information
```
section_schedule_dict = {
    '0_type': 'CLAS',
    '0_days': ['L', 'W'],
    '0_hours': ['2'],
    '1_type': 'CLAS',
    '1_days': ['V'],
    '1_hours': ['2'],
    '2_type': 'AYU',
    '2_days': ['M', 'J'],
    '2_hours': ['4'],
    'len': 3,
    'fail': False
}
```
#### section_class_on_time
```
section_class_on_time = "CLAS FIL2005"
```

### Schedule
```
schedule = "CLAS/L-M:2-3 AYU/W:2"
```
#### schedule_segment
```
schedule_segment = "CLAS/L-M:2-3"
```
#### schedule_segment_type
```
schedule_segment_type = "CLAS"
```
#### schedule_segment_detail
```
schedule_segment_detail = "L-M:2-3"
```
#### schedule_array
```
schedule_array = 
[['', '', '', '', '', ''],
 ['CLAS', '', 'CLAS', '', 'CLAS', ''],
 ['', '', '', '', '', ''],
 ['', 'AYU', '', 'AYU', '', ''],
 ['', '', '', '', '', ''],
 ['', '', '', '', '', ''],
 ['', '', '', '', '', ''],
 ['', '', '', '', '', ''],
 ['', '', '', '', '', '']]
```
#### schedule_number_array
```
schedule_number_array = 
[[0 0 0 0 0 0],
 [1 0 1 0 1 0],
 [0 0 0 0 0 0],
 [0 1 0 1 0 0],
 [0 0 0 0 0 0],
 [0 0 0 0 0 0],
 [0 0 0 0 0 0],
 [0 0 0 0 0 0],
 [0 0 0 0 0 0]]
```

#### Days
```
day = "L"
days = "L M W J V S"
days_dash = "L-M-W-J-V-S"
days_list = ["L", "M", "W", "J", "V", "S"]

day_number = 0 # Monday
days_number_list = [0, 1, 2, 3, 4, 5]
```
#### Hours
```
hour = 1
hours = "1 2 3 4 5 6 7 8 9"
hours_dash = "1-2"
hours_list = [1, 2]
```

### Calendars
#### calendar
```
calendar = {
    "courses_id": ["MAT1630", "FIL2005"],
    "sections_schedule": ["CLAS/L-M:2-3 AYU/W:2", "CLAS/W:1"],
    "sections_nrc_bundle": ["14843/14863", "28764"],
    "sections_nrc_alternative_bundle": ["14848/14868/14841", ""],
    "nrc_active": True,
    "courses_bundle_id": ["MAT1630", "OPT"]
}
```

### Data
#### data: array of a file
#### raw_data: data of a file in str
#### main_data and raw_main_data: the file is data.csv


# Notes
if a function has the comment ###, that means that it hasn't been check yet for VNG following