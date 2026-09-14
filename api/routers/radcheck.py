from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from api.database.session import get_db
from api.models.models import RadCheck  # Pastikan model RadCheck sudah diimpor
from api.schemas.radcheck import RadCheckResponse, RadCheckCreate
from api.utils.security import (
    generate_random_username,
    generate_random_password,
    role_required,
)

router = APIRouter()


@router.post(
    "/users",
    response_model=RadCheckResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate User Radius (Username & Password Random)",
)
async def generate_radius_user(
    request: Request,
    attribute: str = "Cleartext-Password",
    op: str = ":=",
    length: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """
    Membuat 1 pasang kredensial user login hotspot secara otomatis:
    - **Username**: Kombinasi acak unik (di-cek terhadap DB)
    - **Value (Password)**: Password acak
    - **Attribute**: Default `Cleartext-Password` (Sesuai kebutuhan Mikrotik HTTP-CHAP/PAP)
    - **Op**: Default `:=`
    """
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

    return new_radcheck


@router.get(
    "/users",
    response_model=List[RadCheckResponse],
    summary="Melihat Semua Data RadCheck",
)
async def get_all_radcheck(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(role_required(["admin", "superadmin"])),
):
    result = await db.execute(select(RadCheck))
    return result.scalars().all()