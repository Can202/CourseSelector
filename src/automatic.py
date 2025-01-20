# Formatting
# 
import requests
from func import *

# ###
def get_html_content_from_BuscaCursos(Semestre, Sigla, Campus):
    url = f"https://buscacursos.uc.cl/?cxml_semestre={Semestre}&cxml_sigla={Sigla}&cxml_nrc=&cxml_nombre=&cxml_categoria=TODOS&cxml_area_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus={Campus}&cxml_unidad_academica=TODOS&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS&cxml_periodo=TODOS&cxml_escuela=TODOS&cxml_nivel=TODOS#resultados"
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "ERROR"
    return html_content

# ###
def create_csv_from_list(Semestre = "2025-1", courses_names=["MAT1630", "MAT1640", "OFG-FIL2005/VET161G"]):
    csv_content = ""

    for j in range(len(courses_names)):
        loadingAnimation(part=1, i=j, n=len(courses_names), maxPart=1)
        if not("/" in courses_names[j]):
            data = formatting_get_courses(Semestre=Semestre, Sigla=courses_names[j])
            s = courses_names[j]
            for i in range(len(data["schedule"])):
                s += f',${data["nrc"][i]} {data["schedule"][i]}'

            if j != (len(courses_names)-1):
                csv_content += s + "\n"
            else:
                csv_content += s
        else:
            a = courses_names[j].split("-")
            courses_split = a[1].split("/")
            csv_content += a[0]
            s=""
            for k in range(len(courses_split)):
                s=""
                data = formatting_get_courses(Semestre=Semestre, Sigla=courses_split[k])
                for q in range(len(data["schedule"])):
                    s += f',%{courses_split[k]} ${data["nrc"][q]} {data["schedule"][q]}'
                csv_content += s
            if j != (len(courses_names)-1):
                csv_content += "\n"
    loadingAnimation(done=True)

    The_file = open("data.csv", "w")
    print(csv_content, file=The_file)
        


# ###
def get_data_from_html_content(html_content):
    data = {"nrc":[], "schedule":[]}
    total = html_content.count('<tr class="resultadosRowPar">') + html_content.count('<tr class="resultadosRowImpar">')
    
    # Get indexes
    indexes = []
    for i in range(total):
        if i % 2 == 0:
            index = find_kth_occurrence('<tr class="resultadosRowPar">', html_content,(i//2)+1)
            indexes.append(index)
        else:
            index = find_kth_occurrence('<tr class="resultadosRowImpar">', html_content,((i-1)//2)+1)
            indexes.append(index)
    
    # Cut
    content_cuts = []
    for i in range(total):
        if i != (total-1):
            content_cuts.append(html_content[indexes[i]:indexes[i+1]])
        else:
            if len(indexes) != 1:
                content_cuts.append(html_content[indexes[i]:(indexes[i] + (indexes[i] - indexes[i-1]))])
            else:
                content_cuts.append(html_content[indexes[i]:(indexes[i] + 3000)])


    nrcs = []
    schedules = []
    for i in range(total):

        # NRCs
        start_index, end_index = string_between_two_substrings('<td style="font-size:13px;text-align:center;">', "</td>", content_cuts[i])
        nrcs.append(content_cuts[i][start_index:end_index])

        #Schedule
        start_index, end_index = string_between_two_substrings("<table>", "</table>", content_cuts[i])
        table = content_cuts[i][start_index:end_index]
        start_1_text_to_find = '<td style="padding-right:5px;width:50px">\n'
        end_text_to_find = '\n</td>'
        start_2_text_to_find = '<td style="padding-right:5px">\n'

        options = table.count(start_1_text_to_find)
        Complete_Schedule = ""
        for j in range(options):
            if j!=0:
                Complete_Schedule+=" "
            start_index, end_index = string_between_two_substrings(start_1_text_to_find, end_text_to_find, table)
            Schedule = table[start_index:end_index]
            table = table[end_index:]
            start_index, end_index = string_between_two_substrings(start_2_text_to_find, end_text_to_find, table)
            Type = table[start_index:end_index]
            table = table[end_index:]
            if "," in Schedule:
                Schedule = Schedule.replace(",","-")
            if not legit_Schedule(Schedule):
                continue
            Complete_Schedule += Type + "/" + Schedule
        schedules.append(Complete_Schedule)

    data["nrc"] = nrcs
    data["schedule"] = schedules

    return data

# ###
def legit_Schedule(Schedule):
    number = False
    days = False
    for i in range(9):
        if "1 2 3 4 5 6 7 8 9".split(" ")[i] in Schedule:
            number = True
    for i in range(6):
        if "L M W J V S".split(" ")[i] in Schedule:
            days = True
    return (number and days)

# ###
def formatting_get_courses(*,Semestre="", Sigla="", Campus = "San+Joaqu%C3%ADn"):
    html_content = get_html_content_from_BuscaCursos(Semestre, Sigla, Campus)
    data = get_data_from_html_content(html_content)
    return data

# ###
def menu_automatic():

    if not check_website_connection("https://buscacursos.uc.cl"):
        print("No connection to BuscaCursos.")
        print("Check your connection to the internet or check if the BuscaCursos web is working")
        return -1

    print("----- EXAMPLE -----")
    print("Semester: 2025-1")
    print("Courses to look: MAT1630 MAT1640 FIS0152 FIS1523 OPT-FIL2005/VET161G IMT1001")
    print("----- EXAMPLE -----")
    semestre = input("Semester: ")
    courses = input("Courses to look: ")
    course = courses.split(" ")
    create_csv_from_list(Semestre=semestre, courses_names=course)
    print("Done!")
    print("Review the csv file! To check if everything is right.")