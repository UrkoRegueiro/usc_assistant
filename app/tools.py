from typing import Optional, Type, Tuple, Union, Dict
from langchain.tools import BaseTool
from pydantic import BaseModel

from app.models import Estudios, Tipo, Deporte, Idioma
from app.functions import get_areas, get_estudios, get_notas_corte, get_becas, get_calendario, get_deportes, get_idiomas, get_facultades


class AreasTool(BaseTool):
    name = "obten_areas_estudio"
    description = "Obtiene las diferentes areas de estudio que ofrece la universidad. Las areas de estudio estan descritas por 'area', 'url' y 'tipo'."
    def _run(self, tipo: str = "grados"):
        areas = get_areas(tipo)
        return areas

    args_schema: Optional[Type[BaseModel]] = Tipo


class EstudiosTool(BaseTool):
    name = "obten_grados_area"
    description = "Obtiene los grados/carreras o masteres disponibles en un area de estudio. Los estudios estan descritos por 'estudio', 'campus' y 'estudio_url'."

    def _run(self, area_url: str):

        estudios = get_estudios(area_url)
        return estudios

    args_schema: Optional[Type[BaseModel]] = Estudios

class NotasTool(BaseTool):
    name = "obten_notas_corte"
    description = "Obtiene las notas de corte de los diferentes grados. Solo se usa una vez. La nota de corte es la nota mínima requerida para acceder a un grado."

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}
    def _run(self):
        notas = get_notas_corte()
        return notas

class BecasTool(BaseTool):
    name= "obten_becas"
    description = "Obtiene las becas que ofrece la universidad."

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}
    def _run(self):
        becas = get_becas()
        return becas

class CalendarioTool(BaseTool):
    name= "obten_calendario"
    description = "Obtiene el calendario escolar del presente curso."

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}
    def _run(self):
        calendario = get_calendario()
        return calendario


class DeportesTool(BaseTool):
    name = "obten_deportes"
    description = "Obtiene informacion a cerca de deportes en la universidad. La informacion viene descritas por 'titulo_deporte' y 'url_deporte'."

    def _run(self, tipo_deporte: str = "instalaciones"):

        deportes = get_deportes(tipo_deporte)
        return deportes

    args_schema: Optional[Type[BaseModel]] = Deporte


class IdiomasTool(BaseTool):
    name = "obten_info_idiomas"
    description = "Obtiene informacion sobre un curso de idioma en la universidad. La informacion viene descritas por 'curso_nivel', 'periodo', 'campus', 'url_matricula'."

    def _run(self, idioma: str = "todos"):
        cursos_idiomas = get_idiomas(idioma)
        return cursos_idiomas

    args_schema: Optional[Type[BaseModel]] = Idioma


class CentrosTool(BaseTool):
    name = "obten_facultades"
    description = "Obtiene el sitio web de las distintas facultades y escuelas de la universidad. La informacion viene descritas por 'centro' y 'url_centro'."

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}
    def _run(self):
        centros = get_facultades()
        return centros