import re
import requests
from bs4 import BeautifulSoup


usc_url = "https://www.usc.gal"


def get_areas(tipo: str= "grados"):

    areas_url = usc_url + f"/es/estudios/{tipo}"

    response = requests.get(areas_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    areas = soup.find_all("article", class_="is-meta")

    areas_estudio = []

    for area in areas:
        area_info = {"area": area.find("h2", class_="at-title").string,
                     "tipo": tipo,
                     "url": usc_url + f"{area.find('a')['href']}"}

        areas_estudio.append(area_info)

    return areas_estudio


def get_estudios(area_url: str):

    response = requests.get(area_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    estudios = soup.find("div", class_="tier-content").find_all("article", class_="is-studies")

    info_estudios = []

    for estudio in estudios:
        info_estudio = {"estudio": estudio.find("h2").string,
                      "campus": estudio.find("p").string,
                      "estudio_url": usc_url + estudio.find("a")["href"]}

        info_estudios.append(info_estudio)

    return info_estudios


def get_notas_corte():
    notas_url = usc_url + f"/es/admision/graos/notas-corte"

    response = requests.get(notas_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tabla = soup.find_all("table", class_= "ml-table")

    tabla_notas = ""

    for idx, notas in enumerate(tabla):

        if idx==0:
            tabla_notas += "Campus de Santiago: " + notas.get_text()
        else:
            tabla_notas += "Campus de Lugo: " + notas.get_text()

    return tabla_notas


def get_becas():
    becas_url = usc_url + f"/es/servicios/area/becas-ayudas/becas-ayudas"

    response = requests.get(becas_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    attrs = {"id": "block-usc-theme-content"}
    info_becas = soup.find("div", attrs=attrs)

    informacion_becas = []

    seccion_1 = info_becas.find_all("article", class_="is-program")
    for beca in seccion_1:
        informacion_beca = {"categoria": info_becas.find("div", class_="at-lead-text").find("p").get_text(),
                            "titulo": beca.find("span", class_="title-inner-wrapper").get_text(),
                            "descripcion": beca.find("div", class_="at-text").get_text(),
                            "url_beca": usc_url + beca.find("a", class_="banner-link")["href"]}

        informacion_becas.append(informacion_beca)

    seccion_2 = info_becas.find_all("div", class_="col-lg-6")
    for beca in seccion_2:
        informacion_beca = {"categoria": beca.find("h2", class_="tier-title").get_text(),
                            "titulo": beca.find("span", class_="title-inner-wrapper").get_text(),
                            "descripcion": beca.find("div", class_="at-text").get_text(),
                            "url_beca": usc_url + beca.find("a", class_="banner-link")["href"]}

        informacion_becas.append(informacion_beca)

    return informacion_becas

def get_calendario():
    calendario_url = usc_url + f"/es/calendario-academico"

    response = requests.get(calendario_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    attrs = {"id": "block-usc-theme-content"}
    info_calendario = soup.find("div", attrs=attrs).get_text()

    return info_calendario

def get_deportes(tipo_deporte: str = "instalaciones"):

    if tipo_deporte == 'instalaciones':
        deportes_url = usc_url + f"/es/servicios/area/deporte/{tipo_deporte}"

        response = requests.get(deportes_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        deportes = soup.find_all("article", class_="is-services")

        info_deportes = []

        for deporte in deportes:
            info_deporte = {"titulo_deporte": deporte.find("span", class_="title-inner-wrapper").get_text(),
                            "url_deporte": usc_url + deporte.find("a", class_="banner-link")["href"]}

            info_deportes.append(info_deporte)

    if tipo_deporte == 'actividades':
        deportes_url_solitario = usc_url + f"/es/servicios/area/deporte/'practica-libre'"
        deportes_url_grupo = usc_url + f"/es/servicios/area/deporte/actividad-dirigida-escuelas"

        urls = [deportes_url_solitario, deportes_url_grupo]
        info_deportes = []

        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            deportes = soup.find_all("article", class_="is-services")

            for deporte in deportes:
                info_deporte = {"titulo_deporte": deporte.find("span", class_="title-inner-wrapper").get_text(),
                                "url_deporte": deporte.find("a", class_="banner-link")["href"]}

                info_deportes.append(info_deporte)

    return info_deportes


def get_idiomas(idioma_elegido: str = "todos"):

    idioma_url = usc_url + "/gl/centro/centro-linguas-modernas/linguas"

    response = requests.get(idioma_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    idiomas = soup.find("div", class_="tier-content").find_all("article", class_="ml-banner")

    info_idiomas = []
    for idioma in idiomas:
        info_idioma = {"curso": idioma.find("h2", class_="at-title").get_text(),
                       "url_idioma": usc_url + idioma.find("a")["href"]}

        info_idiomas.append(info_idioma)

    lista_idiomas = [idioma.find("h2", class_="at-title").get_text() for idioma in idiomas]
    indices = [i for i in range(len(lista_idiomas))]
    dic_idiomas = {lengua: idx for lengua, idx in zip(lista_idiomas, indices)}

    if idioma_elegido == "todos":
        return info_idiomas

    else:
        indice = dic_idiomas[idioma_elegido]
        url_idioma_elegido = info_idiomas[indice]["url_idioma"]
        response_idioma_elegido = requests.get(url_idioma_elegido)
        soup_idioma_elegido = BeautifulSoup(response_idioma_elegido.text, 'html.parser')
        attrs = {"id": "block-usc-theme-content"}
        attrs_1 = {"id": "clm-formative-activities"}
        cursos_idioma_elegido = soup_idioma_elegido.find("div", attrs= attrs).find("div", attrs= attrs_1).find_all("article", class_= "ml-academic-subject")

        info_niveles_idioma = []
        for nivel_idioma in cursos_idioma_elegido:

            matricula = nivel_idioma.find_all("dl")[2]
            dts_matricula = matricula.find_all("dt")
            dds_matricula = matricula.find_all("dd")
            for dt, dd in zip(dts_matricula,dds_matricula):
                if dt.string == "Acceso matrícula":
                    enlace_matricula = dd.find("a")["href"]

            info_nivel_idioma = {"curso_nivel": idioma_elegido + " " + nivel_idioma.find("h3", class_= "at-title").string.split("|")[0],
                                 "periodo": nivel_idioma.find("h3", class_= "at-title").string.split("|")[2],
                                 "campus" : nivel_idioma.find("h3", class_= "at-title").string.split("|")[3],
                                 "url_matricula": enlace_matricula}
            info_niveles_idioma.append(info_nivel_idioma)

        return info_niveles_idioma




def get_facultades():
    centros_url = usc_url + "/es/centro"

    response = requests.get(centros_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    attrs = {"id": "block-centros"}
    centros = soup.find("div", attrs=attrs).find_all("article", class_="ml-banner")

    info_centros = []

    for centro in centros:
        info_centro = {"centro": centro.find("h2", class_="at-title").get_text(),
                       "url_centro": usc_url + centro.find("a")["href"]}
        info_centros.append(info_centro)

    return info_centros

