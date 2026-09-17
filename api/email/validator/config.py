import os
from pathlib import Path

# Mendapatkan direktori tempat config.py berada (api/email/validator)
BASE_DIR = Path(__file__).resolve().parent

# Arahkan ke folder data (api/email/data)
DATA_DIR = BASE_DIR.parent / "data"

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))

# Gunakan path absolut yang sudah dihitung
DISPOSABLE_FILE = os.getenv("DISPOSABLE_FILE", str(DATA_DIR / "disposable.txt"))
FREE_FILE = os.getenv("FREE_FILE", str(DATA_DIR / "free.txt"))
SKIPLIST_FILE = os.getenv("SKIPLIST_FILE", str(DATA_DIR / "skiplist.txt"))

VALIDATION_MODE = os.getenv("VALIDATION_MODE", "public").lower()
MAX_ATTEMPT = int(os.getenv("MAX_ATTEMPT", 3))
BLOCK_TTL = int(os.getenv("BLOCK_TTL", 300))  # 5 menit
DOMAIN_CACHE_TTL = int(os.getenv("DOMAIN_CACHE_TTL", 86400))  # 24 jam