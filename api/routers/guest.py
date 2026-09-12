from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from api.database.session import get_db
from api.models.models import Guest
from api.schemas.guest import (
    GuestCreate,
    GuestUpdate,
    GuestResponse
)


router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ============================================================
# CREATE GUEST
# ============================================================
@router.post(
    "/",
    response_model=GuestResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_guest(
    guest_in: GuestCreate,
    db: AsyncSession = Depends(get_db)
):

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

    # --------------------------------------------------------
    # Cek username
    # --------------------------------------------------------
    result = await db.execute(
        select(Guest).where(
            Guest.username == guest_in.username
        )
    )

    existing_username = result.scalar_one_or_none()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah digunakan."
        )

    # --------------------------------------------------------
    # Hash password
    # --------------------------------------------------------
    hashed_password = pwd_context.hash(
        guest_in.password
    )

    # --------------------------------------------------------
    # Buat Guest
    # --------------------------------------------------------
    new_guest = Guest(
        name=guest_in.name,
        email=guest_in.email,
        phone=guest_in.phone,
        username=guest_in.username,
        password=hashed_password
    )

    db.add(new_guest)

    await db.commit()

    await db.refresh(new_guest)

    return new_guest


# ============================================================
# GET ALL GUEST
# ============================================================
@router.get(
    "/",
    response_model=list[GuestResponse]
)
async def get_guests(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Guest)
    )

    guests = result.scalars().all()

    return guests


# ============================================================
# GET GUEST BY ID
# ============================================================
@router.get(
    "/{guest_id}",
    response_model=GuestResponse
)
async def get_guest(
    guest_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Guest).where(
            Guest.id == guest_id
        )
    )

    guest = result.scalar_one_or_none()

    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest tidak ditemukan."
        )

    return guest


# ============================================================
# UPDATE GUEST
# ============================================================
@router.put(
    "/{guest_id}",
    response_model=GuestResponse
)
async def update_guest(
    guest_id: int,
    guest_in: GuestUpdate,
    db: AsyncSession = Depends(get_db)
):

    # --------------------------------------------------------
    # Cari Guest
    # --------------------------------------------------------
    result = await db.execute(
        select(Guest).where(
            Guest.id == guest_id
        )
    )

    guest = result.scalar_one_or_none()

    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest tidak ditemukan."
        )

    # --------------------------------------------------------
    # Data yang dikirim
    # --------------------------------------------------------
    update_data = guest_in.model_dump(
        exclude_unset=True
    )

    # --------------------------------------------------------
    # Cek email jika diubah
    # --------------------------------------------------------
    if "email" in update_data:

        result = await db.execute(
            select(Guest).where(
                Guest.email == update_data["email"],
                Guest.id != guest_id
            )
        )

        existing_email = result.scalar_one_or_none()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email sudah digunakan."
            )

    # --------------------------------------------------------
    # Cek username jika diubah
    # --------------------------------------------------------
    if "username" in update_data:

        result = await db.execute(
            select(Guest).where(
                Guest.username == update_data["username"],
                Guest.id != guest_id
            )
        )

        existing_username = result.scalar_one_or_none()

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username sudah digunakan."
            )

    # --------------------------------------------------------
    # Hash password jika password diubah
    # --------------------------------------------------------
    if "password" in update_data:

        update_data["password"] = pwd_context.hash(
            update_data["password"]
        )

    # --------------------------------------------------------
    # Update object
    # --------------------------------------------------------
    for field, value in update_data.items():
        setattr(guest, field, value)

    await db.commit()

    await db.refresh(guest)

    return guest


# ============================================================
# DELETE GUEST
# ============================================================
@router.delete(
    "/{guest_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_guest(
    guest_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Guest).where(
            Guest.id == guest_id
        )
    )

    guest = result.scalar_one_or_none()

    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest tidak ditemukan."
        )

    await db.delete(guest)

    await db.commit()

    return None