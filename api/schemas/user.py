from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ==========================================
# 1. BASE SCHEMA (Shared Properties)
# ==========================================
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=300, example="John Doe")
    username: str = Field(..., min_length=3, max_length=100, example="johndoe")
    email: EmailStr = Field(..., example="john@example.com")
    phone: Optional[str] = Field(None, max_length=20, example="081234567890")
    role: str = Field(default="user", max_length=50, example="admin")


# ==========================================
# 2. CREATE SCHEMA (Payload Input POST /users)
# ==========================================
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255, example="Secret123!")


# ==========================================
# 3. UPDATE SCHEMA (Payload Input PUT/PATCH /users/{id})
# ==========================================
class UserUpdate(BaseModel):
    # Semua dibuat Optional agar frontend bisa mengupdate sebagian kolom saja
    name: Optional[str] = Field(None, min_length=2, max_length=300)
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    role: Optional[str] = Field(None, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=255)


# ==========================================
# 4. RESPONSE SCHEMA (Output dari Endpoint)
# ==========================================
class UserResponse(UserBase):
    id: int
    email_verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        # PENTING: Mengizinkan Pydantic membaca data dari objek SQLAlchemy ORM
        orm_mode = True