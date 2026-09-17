import json
from api.email.validator import syntax, mx, disposable, free, skiplist
from api.email.validator.cache.redis_client import r
from api.email.validator.config import CACHE_TTL
from api.email.validator.config import VALIDATION_MODE, DOMAIN_CACHE_TTL

def validate_email(email: str):
    cache_key = f"email:{email}"

    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    # 🔥 1. cek syntax dulu (fail fast)
    syntax_ok = syntax.check(email)

    if not syntax_ok:
        result = {
            "email": email,
            "checks": {
                "syntax": False,
                "mx": False,
                "disposable": False,
                "free": False,
                "skiplist": False
            },
            "is_valid": False,
            "reason": "invalid_format"
        }

        r.setex(cache_key, CACHE_TTL, json.dumps(result))
        return result

    # 🔥 2. aman ambil domain
    domain = email.split("@")[1].strip().lower()

    domain_key = f"domain:{domain}"
    domain_cached = r.get(domain_key)

    if domain_cached:
        domain_checks = json.loads(domain_cached)
        result = {
            "email": email,
            "checks": {
                "syntax": syntax.check(email),
                **domain_checks
            },
        }
        result["is_valid"] = is_valid_email(result['checks'])
        r.setex(cache_key, CACHE_TTL, json.dumps(result))
        return result
    else:
        domain_checks = {
            "mx": mx.check(domain),
            "disposable": disposable.check(domain),
            "free": free.check(domain),
            "skiplist": skiplist.check(domain)
        }

        r.setex(domain_key, DOMAIN_CACHE_TTL, json.dumps(domain_checks))

    # 🔥 3. lanjut validasi domain
    result = {
        "email": email,
        "checks": {
            "syntax": True,
            "mx": mx.check(domain),
            "disposable": disposable.check(domain),
            "free": free.check(domain),
            "skiplist": skiplist.check(domain)
        }
    }

    result["is_valid"] = is_valid_email(result['checks'])

    r.setex(cache_key, CACHE_TTL, json.dumps(result))
    return result

def is_valid_email(checks):
    if VALIDATION_MODE == "strict":
        return (
            checks["syntax"]
            and checks["mx"]
            and not checks["disposable"]
            and not checks["free"]
            and not checks["skiplist"]
        )

    # default = public
    return (
        checks["syntax"]
        and checks["mx"]
        and not checks["disposable"]
    )