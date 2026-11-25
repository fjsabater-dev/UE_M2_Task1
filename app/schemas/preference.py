from pydantic import BaseModel, Field
from typing import Literal # Restrict the value of a field to a specific set of string

class PreferenceCreate(BaseModel):
    type: Literal["streamer", "game"] # 422 if not one of the two values
    name: str = Field(..., min_length=1, max_length=100)