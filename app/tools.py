from typing import Optional, Type, List, Tuple, Union, Dict

from langchain.tools import BaseTool
from pydantic import BaseModel

from app.models import Estudios, Tipo

from app.functions import get_areas, get_estudios, get_notas_corte


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

