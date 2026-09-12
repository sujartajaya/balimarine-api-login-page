from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# =========================
# ClientDevice - Base
# =========================
class ClientDeviceBase(BaseModel):
    mac_add: Optional[str] = None
    os_client: Optional[str] = None
    browser_client: Optional[str] = None
    device_client: Optional[str] = None
    brand_client: Optional[str] = None
    model_client: Optional[str] = None
    device_type: Optional[str] = None


# =========================
# ClientDevice - Create
# =========================
class ClientDeviceCreate(ClientDeviceBase):
    guest_id: int


# =========================
# ClientDevice - Update
# =========================
class ClientDeviceUpdate(BaseModel):
    guest_id: Optional[int] = None
    mac_add: Optional[str] = None
    os_client: Optional[str] = None
    browser_client: Optional[str] = None
    device_client: Optional[str] = None
    brand_client: Optional[str] = None
    model_client: Optional[str] = None
    device_type: Optional[str] = None


# =========================
# ClientDevice - Response
# =========================
class ClientDeviceResponse(ClientDeviceBase):
    id: int
    guest_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)