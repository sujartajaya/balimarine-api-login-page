from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    MIKROTIK_HOST: str
    MIKROTIK_USERNAME: str
    MIKROTIK_PASSWORD: str
    MIKROTIK_PORT: int = 8729
    MIKROTIK_SSL: bool = True
    
    class Config:
        env_file = ".env"  # otomatis baca dari .env

settings = Settings()
