from typing import Optional, Type, List, Tuple, Union, Dict

from langchain.tools import BaseTool
from pydantic import BaseModel

from app.models import Grados

from app.functions import get_areas, get_degrees


class AreasTool(BaseTool):
    name = "obten_areas_estudio"
    description = "Obtiene las diferentes areas de estudio que ofrece la universidad. Las areas de estudio estan descritas por 'area' y 'url'."

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}
    def _run(self):
        areas = get_areas()
        return areas

class GradosTool(BaseTool):
    name = "obten_grados_area"
    description = "Obtiene los grados o carreras disponibles en un area de estudio. Los grados estan descritos por 'grado', 'campus' y 'grado_url'."

    def _run(self, area_url: str):

        grados = get_degrees(area_url)
        return grados

    args_schema: Optional[Type[BaseModel]] = Grados

