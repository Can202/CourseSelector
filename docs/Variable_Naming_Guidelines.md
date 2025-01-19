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

### Calendars
#### calendar
```
calendar = {
    "courses_id": ["MAT1630", "FIL2005"],
    "sections_nrc_bundle": ["14843/14863", "28764"],
    "sections_nrc_alternative_bundle": ["14848/14868/14841", ""],
    "nrc_active": True,
    "courses_bundle_id": ["MAT1630", "OPT"]
}
```