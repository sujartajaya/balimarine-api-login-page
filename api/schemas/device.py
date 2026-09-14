from pydantic import BaseModel, Field
from typing import Optional

class DeviceResponse(BaseModel):
    os_client: Optional[str] = None
    browser_client: Optional[str] = None
    device_client: Optional[str] = None
    brand_client: Optional[str] = None
    model_client: Optional[str] = None
    device_type: Optional[str] = None
    
class DeviceCheck(BaseModel):
    useragent: str
    