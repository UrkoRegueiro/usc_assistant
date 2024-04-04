import requests
from bs4 import BeautifulSoup


usc_url = "https://www.usc.gal"


def get_areas():

    areas_url = usc_url + "/es/estudios/grados"

    response = requests.get(areas_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    areas = soup.find_all("article", class_="is-meta")

    areas_estudio = []

    for area in areas:
        area_info = {"area": area.find("h2", class_="at-title").string,
                     "url": usc_url + f"{area.find('a')['href']}"}

        areas_estudio.append(area_info)

    return areas_estudio


def get_degrees(area_url: str = None):
    response = requests.get(area_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    grados = soup.find("div", class_="tier-content").find_all("article", class_="is-studies")

    info_grados = []

    for grado in grados:
        info_grado = {"grado": grado.find("h2").string,
                      "campus": grado.find("p").string,
                      "grado_url": usc_url + grado.find("a")["href"]}

        info_grados.append(info_grado)

    return info_grados