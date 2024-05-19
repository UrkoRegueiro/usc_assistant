from pydantic import BaseModel, Field

class Tipo(BaseModel):
    tipo: str = Field(default="grados",
                      description="El tipo de estudio. Puede ser uno de los siguientes: 'grados', 'masteres', 'doctorados'. Por defecto a 'grados'")


class Estudios(BaseModel):
    area_url: str = Field(...,
                          description="La url para acceder a los grados/carreras o masteres disponibles en un area de estudio.")


class Deporte(BaseModel):
    tipo_deporte: str = Field(default="instalaciones",
                              description="Los diferentes tipos de actividad deportiva. SOLO puede ser uno de los siguientes valores: 'instalaciones', 'actividades'. Por defecto a 'instalaciones'")


class Idioma(BaseModel):
    idioma: str = Field(default="todos",
                        description="Los diferentes idiomas que se enseñan en la universidad. Puede ser uno de los siguientes: 'todos', 'Galego', 'Español', 'Alemán', 'Catalán', 'Francés', 'Inglés', 'Italiano', 'Portugués', 'Checo'. Por defecto a 'todos'")
