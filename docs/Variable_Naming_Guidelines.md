# Variable Naming Guidelines (VNG)

We have calendars, courses and sections.

## Types of information
### Courses
#### course_id: (str) The id of a course (e.g. "MAT1630" or "FIL2005")
#### course_bundle_id: (str) The id of a bundle of courses (e.g. "MAT1630" or "OPT-FIL2005/VET161G")
#### course_bundle_name: (str) The name of a bundle of courses (e.g. "MAT1630" or "OPT")

### Sections
#### section_nrc
#### section_nrc_bundle
#### section_nrc_alternative_bundle

### Calendars
#### calendar: (dict)
```
calendar = {
    "courses_id": ["MAT1630", "FIL2005"],
    "sections_nrc_bundle": ["14843/14863", "28764"],
    "sections_nrc_alternative_bundle": ["14848/14868/14841", ""],
    "nrc_active": True,
    "courses_bundle_id": ["MAT1630", "OPT"]
}
```