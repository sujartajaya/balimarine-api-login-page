from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

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
    mac_add: Optional[str] = None

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
    password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# ==========================================
# 1. BASE SCHEMA (Shared Properties)
# ==========================================
class RadCheckBase(BaseModel):
    username: str = Field(
        ..., 
        max_length=64, 
        description="Username akun radius/guest", 
        example="guest_user_1"
    )
    attribute: str = Field(
        ..., 
        max_length=64, 
        description="Attribute FreeRADIUS (misal: Cleartext-Password, Expiration)", 
        example="Cleartext-Password"
    )
    op: str = Field(
        default="==", 
        max_length=2, 
        description="Operator FreeRADIUS (misal: ==, :=, +=)", 
        example=":="
    )
    value: str = Field(
        ..., 
        max_length=253, 
        description="Nilai dari attribute (misal: password123, 11 Sep 2026)", 
        example="SecretPass123"
    )

# ==========================================
# 2. CREATE SCHEMA (Payload Input POST)
# ==========================================
class RadCheckCreate(RadCheckBase):
    pass


# ==========================================
# 3. UPDATE SCHEMA (Payload Input PUT/PATCH)
# ==========================================
class RadCheckUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=64)
    attribute: Optional[str] = Field(None, max_length=64)
    op: Optional[str] = Field(None, max_length=2)
    value: Optional[str] = Field(None, max_length=253)


# ==========================================
# 4. RESPONSE SCHEMA (Output dari Endpoint)
# ==========================================
class RadCheckResponse(RadCheckBase):
    id: int

    class Config:
        orm_mode = True