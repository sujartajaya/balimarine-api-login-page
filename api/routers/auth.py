from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from api.database.session import get_db  # Import get_db async Anda
from api.models.models import User
from api.schemas.auth import UserRegister
from api.schemas.user import UserResponse

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserRegister, 
    db: AsyncSession = Depends(get_db)  # Inject AsyncSession
):
    # 1. Cek Email (Gunakan await & select)
    query_email = await db.execute(select(User).where(User.email == user_in.email))
    existing_email = query_email.scalar_one_or_none()
    
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar, silakan gunakan email lain."
        )

    # 2. Cek Username (Gunakan await & select)
    query_username = await db.execute(select(User).where(User.username == user_in.username))
    existing_username = query_username.scalar_one_or_none()
    
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah digunakan, silakan pilih username lain."
        )

    # 3. Hash Password
    hashed_password = pwd_context.hash(user_in.password)

    # 4. Buat Instance Model
    new_user = User(
        name=user_in.name,
        username=user_in.username,
        email=user_in.email,
        password=hashed_password,
        phone=user_in.phone,
        role="user"
    )

    # 5. Simpan ke Database (Gunakan await db.commit() & await db.refresh())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user