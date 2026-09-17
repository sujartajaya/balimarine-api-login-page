from fastapi import APIRouter
from api.routers import auth, guest, radcheck, hotspot, email


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(guest.router, prefix="/guests", tags=["Guests"])
api_router.include_router(hotspot.router, prefix="/hotspot", tags=["Hotspot"])
api_router.include_router(email.app, prefix="/email", tags=["Email"])
