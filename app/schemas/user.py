from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50) # ... means required field
    email: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=0, le=120)

class UserUpdate(BaseModel):
    username: str = Field(None, min_length=1, max_length=50) # None means optional field
    email: str = Field(None, min_length=1, max_length=50)
    age: int = Field(None, ge=0, le=120)