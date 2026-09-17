from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from api.database.session import get_db
from api.models.models import RadCheck, Guest # Pastikan model RadCheck sudah diimpor
# from api.schemas.radcheck import RadCheckResponse, RadCheckCreate
from api.schemas.hotspot import (
    GuestCreate,
    GuestUpdate,
    GuestResponse,
    RadCheckResponse,
    RadCheckCreate
)

from api.utils.security import (
    generate_random_username,
    generate_random_password,
    role_required,
)

router = APIRouter()

@router.post(
    "/register",
        response_model=GuestResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Register guest (name, email, phone)",
)

async def hotspot_register(
    request: Request,
    guest_in: GuestCreate,
    db: AsyncSession = Depends(get_db),
):
            attribute = "Cleartext-Password"
            op = ":="
            length = 10 
    
            # --------------------------------------------------------
            # Cek email
            # --------------------------------------------------------
            result = await db.execute(
                select(Guest).where(
                    Guest.email == guest_in.email
                )
            )
    
            existing_email = result.scalar_one_or_none()
            
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email sudah terdaftar."
                )
    
            # 1. Generate Username Unik & Password Random via utils/security.py
            random_username = await generate_random_username(db, length=length)
            random_password = generate_random_password(length=length)
    
            # 2. Buat Record untuk tabel RadCheck
            new_radcheck = RadCheck(
                username=random_username,
                attribute=attribute,
                op=op,
                value=random_password,
            )
        
            # 3. Simpan ke MariaDB
            db.add(new_radcheck)
            await db.commit()
            await db.refresh(new_radcheck)    
    
            new_guest = Guest (
                    name=guest_in.name,
                    email=guest_in.email,
                    phone=guest_in.phone,
                    username=random_username,
                    password=random_password,
            )
            db.add(new_guest)
            await db.commit()
            await db.refresh(new_guest)

            # Penambahan device


            return new_guest