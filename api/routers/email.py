from fastapi import APIRouter
from pydantic import BaseModel
from api.email.validator.services.validator_service import validate_email
from api.email.validator import disposable, free, skiplist
from api.email.validator.config import DISPOSABLE_FILE, FREE_FILE, SKIPLIST_FILE, MAX_ATTEMPT, BLOCK_TTL
from api.email.validator.cache.redis_client import r, set_block, is_blocked

app = APIRouter()

# init data saat startup
disposable.init(DISPOSABLE_FILE)
free.init(FREE_FILE)
skiplist.init(SKIPLIST_FILE)

class EmailRequest(BaseModel):
    email: str
    mac: str

@app.post("/validate")
def validate(req: EmailRequest):
    """
        # Validasi email dengan mengirimkan:
        - **Email**: alamat email yang mau divalidasi
        - **Mac Address**: mac address perangkat, bisa didapat dari saat pertama kali user konek akan dikirimkan ke link login
        # Result:
        - ** **

    """
    mac = req.mac
    email = req.email

    # 🚫 cek apakah sedang diblok
    if is_blocked(mac):
        ttl = r.ttl(f"block:{mac}")
        return {
            "email": email,
            "mac": mac,
            "blocked": True,
            "retry_after": ttl,
            "message": "Too many attempts."
        }

    # 🔍 jalankan validator
    result = validate_email(email)

    # ❌ kalau tidak valid → increment counter
    if not result["is_valid"]:
        key = f"attempt:{mac}"
        attempt = r.incr(key)

        # set expire kalau pertama kali
        if attempt == 1:
            r.expire(key, BLOCK_TTL)

        # 🚨 kalau melebihi limit → block
        if attempt >= MAX_ATTEMPT:
            set_block(mac, BLOCK_TTL)

            # 🔥 hapus attempt biar tidak numpuk
            r.delete(key)

            return {
                "email": email,
                "mac": mac,
                "blocked": True,
                "message": "Too many attempts. You are blocked for 5 minutes."
            }

        return {
            **result,
            "attempt": attempt,
            "remaining": MAX_ATTEMPT - attempt
        }

    # ✅ kalau valid → reset counter
    r.delete(f"attempt:{mac}")

    return {
        **result,
        "attempt": 0
    }