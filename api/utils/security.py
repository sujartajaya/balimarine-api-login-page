from passlib.hash import bcrypt
from api.models.models import User, Guest, ServiceRenewalModel
import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.database.session import get_db
from api.config.system import settings

def hash_password(password: str) -> str:
    hashed = bcrypt.using(rounds=10).hash(password)
    # Ganti prefix $2b$ jadi $2y$ agar identik dengan Laravel
    return hashed.replace("$2b$", "$2y$")

def verify_password(password: str, hashed: str) -> bool:
    # Laravel akan pakai bcrypt verify, jadi di Python ini untuk cek internal saja
    return bcrypt.verify(password, hashed.replace("$2y$", "$2b$"))

async def create_unique_token(db) -> str:
    while True:
        # Bagian A: angka acak 6 digit
        part_a = ''.join(random.choices(string.digits, k=8))
        # Bagian B: huruf besar saja
        part_b = ''.join(random.choices(string.ascii_uppercase, k=8))
        # Bagian C: huruf besar + angka
        part_c = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        token = f"{part_a}-{part_b}-{part_c}"
        # Cek apakah token sudah ada di database
        # Query async untuk cek token
        result = await db.execute(
            select(User).where(User.remember_token == token)
        )
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            return token

async def generate_random_service_code(db) -> str:
    while True:
        # Bagian A: angka acak 6 digit
        part_a = ''.join(random.choices(string.digits, k=8))
        # Bagian B: huruf besar saja
        part_b = ''.join(random.choices(string.ascii_uppercase, k=8))
        # Bagian C: huruf besar + angka
        part_c = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # Bagian D: angka acak 6 digit
        part_d = ''.join(random.choices(string.digits, k=8))

        token = f"{part_a}-{part_b}-{part_c}-{part_d}"
        # Cek apakah token sudah ada di database
        # Query async untuk cek token
        result = await db.execute(
            select(ServiceRenewalModel).where(ServiceRenewalModel.service_code == token)
        )

        existing_code = result.scalar_one_or_none()

        if not existing_code:
            return token

async def generate_random_username(db, length: int = 10) -> str:
    while True:
        """Buat username random kombinasi huruf besar, kecil, angka."""
        chars = string.ascii_letters + string.digits
        username = ''.join(random.choices(chars, k=length))
        result = await db.execute(select(Guest).where(Guest.username == username))
        exist_username = result.scalar_one_or_none()
        if not exist_username:
            return username

def generate_random_password(length: int = 10) -> str:
    """Buat password random kombinasi huruf besar, kecil, angka, dan karakter khusus."""
    special_chars = "!#*&^?<>[]{}/~"
    chars = string.ascii_letters + string.digits + special_chars
    return ''.join(random.choices(chars, k=length))



from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = settings.SECRET_KEY  # ganti dengan yang aman, simpan di env
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # berisi user_id, role, dll
    except JWTError:
        return None

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from api.database.session import get_db
from api.models.models import User
from api.utils.security import SECRET_KEY, ALGORITHM
from fastapi import Request

# TAMABAG class baru
# 1. Buat class custom yang meng-override fungsi call bawaan
class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # KUNCI PERBAIKAN: Jika metodenya OPTIONS, kembalikan None tanpa cek token
        if request.method == "OPTIONS":
            return None
        # Jika metode lain (GET, POST, dll), jalankan pengecekan token standar bawaan FastAPI
        return await super().__call__(request)

# 2. Ganti instansiasi lama dengan class custom yang baru
security = CustomHTTPBearer(auto_error=False) 
# Catatan: auto_error=False mencegah FastAPI melempar 403 otomatis sebelum masuk ke internal logika Anda

# security = HTTPBearer()




def role_required(allowed_roles: List[str]):
    """
    Middleware dependency untuk memvalidasi JWT dan role user.
    allowed_roles -> daftar role yang diizinkan mengakses endpoint.
    """
    async def verify_role(
        request: Request = None,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
        db: AsyncSession = Depends(get_db)
    ):
        if request and request.method == "OPTIONS":
            return None

        # Jika bukan OPTIONS dan token tidak dikirim oleh frontend
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak ditemukan, silakan login kembali.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        token = credentials.credentials

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")  # disesuaikan dengan token
            role: str = payload.get("role")
            # print(f"Hasil cek role:\nUSERNAME = {username}\nRole = {role}")
            if username is None or role is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token tidak valid",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak valid atau sudah kedaluwarsa",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Validasi role
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Anda tidak memiliki hak akses",
            )

        # Validasi user di database
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Pengguna tidak ditemukan",
            )

        return user  # Bisa dipakai di endpoint

    return verify_role
