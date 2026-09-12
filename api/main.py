from __future__ import annotations
from fastapi import FastAPI
from api.routers.api import api_router

app = FastAPI(title="Bali Marine Service API",
    description="""
## Selamat Datang di Dokumentasi API Bali Marine Service 🚀

API ini menyediakan layanan backend untuk autentikasi dan manajemen sistem pengguna.

### Panduan Penggunaan:
* **Autentikasi**: Gunakan endpoint `/api/auth/login` untuk mendapatkan `access_token`.
* **Authorization**: Masukkan token pada tombol **Authorize** di pojok kanan atas dengan format `Bearer <token>`.
* **Register Guest**: Gunakan endpoint **POST** `/api/guest` untuk register guest pada halaman login page.
* **Format Response**: Semua response menggunakan format JSON standar.
    """,
    version="1.0.0",)


@app.get("/")
async def root():
    return {"info": "Selamat Datang!"}

app.include_router(api_router, prefix="/api")

