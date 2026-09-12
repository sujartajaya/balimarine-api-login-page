from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=300, example="Budi Santoso")
    username: str = Field(..., min_length=3, max_length=100, example="budis")
    email: EmailStr = Field(..., example="budi@example.com")
    password: str = Field(..., min_length=8, max_length=255, example="Password123!")
    phone: Optional[str] = Field(None, max_length=20, example="08123456789")