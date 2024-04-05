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
    becas_url = usc_url + f"/es/admision/bolsas"


