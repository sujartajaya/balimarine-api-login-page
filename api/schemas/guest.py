from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# ============================================================
# Guest Base
# ============================================================
class GuestBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    username: str


# ============================================================
# Guest Create
# ============================================================
class GuestCreate(GuestBase):
    password: str


# ============================================================
# Guest Update
# ============================================================
class GuestUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


# ============================================================
# Guest Response
# ============================================================
class GuestResponse(GuestBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True