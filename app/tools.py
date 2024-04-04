from typing import Optional, Type, List, Tuple, Union, Dict

from langchain.tools import BaseTool
from pydantic import BaseModel

#from app.models import

from app.functions import get_areas


class AreasTool(BaseTool):
    name = "obten_areas_estudio"
    description = "Obtiene las diferentes areas de estudio que ofrece la universidad. Las areas de estudio estan descritas por 'area' y 'url'."

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}
    def _run(self):
        areas = get_areas()
        return areas

