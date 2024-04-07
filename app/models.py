from pydantic import BaseModel, Field

class Tipo(BaseModel):
    tipo: str = Field(default="grados",
                      description="El tipo de estudio. Puede ser uno de los siguientes: 'grados', 'masteres'. Por defecto a 'grados'")


class Estudios(BaseModel):
    area_url: str = Field(...,
                          description="La url para acceder a los grados/carreras o masteres disponibles en un area de estudio.")


class Deporte(BaseModel):
    tipo_deporte: str = Field(default="instalaciones",
                              description="Los diferentes tipos de actividad deportiva. Puede ser uno de los siguientes: 'instalaciones', 'actividades'. Por defecto a 'instalaciones'")

