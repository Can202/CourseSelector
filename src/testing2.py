import requests
from func import *
import time

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

from selenium import webdriver

def get_html_content_from_BuscaCursos2(Semestre, Sigla, Campus):
    url = f"https://buscacursos.uc.cl/?cxml_semestre={Semestre}&cxml_sigla={Sigla}&cxml_nrc=&cxml_nombre=&cxml_categoria=TODOS&cxml_area_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus={Campus}&cxml_unidad_academica=TODOS&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS&cxml_periodo=TODOS&cxml_escuela=TODOS&cxml_nivel=TODOS#resultados"
    driver = webdriver.Firefox()

    try:
        driver.get(url)
        html_content = driver.page_source
    except Exception as e:
        print(f"An error occurred: {e}")
        return "ERROR"
    finally:
        driver.quit()

    return html_content

print(get_html_content_from_BuscaCursos2("2026-1","MAT1610","San+Joaqu%C3%ADn"))