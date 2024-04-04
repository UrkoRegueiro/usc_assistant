from pydantic import BaseModel, Field


class Grados(BaseModel):
    url: str = Field(..., description="The url to access the information schema")
