from pydantic import BaseModel, Field


class Grados(BaseModel):
    area_url: str = Field(..., description="La url para acceder a los grados o carreras disponibles en un area de estudio.")
