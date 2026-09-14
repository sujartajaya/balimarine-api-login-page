from fastapi import APIRouter
from api.routers import auth, guest, radcheck


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(guest.router, prefix="/guests", tags=["Guests"])
api_router.include_router(radcheck.router, prefix="/hotspot", tags=["Hotspot"])