import redis
from api.email.validator.config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def set_block(mac: str, ttl: int = 300):
    key = f"block:{mac}"
    r.setex(key, ttl, "1")

def is_blocked(mac: str):
    key = f"block:{mac}"
    return r.exists(key)