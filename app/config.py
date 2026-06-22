from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./assistant.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    WEBHOOK_SECRET: SecretStr
    MACRODROID_API_KEY: SecretStr
    ALLOWED_TELEGRAM_IDS: str
    TELEGRAM_BOT_TOKEN: SecretStr
    GEMINI_API_KEY: SecretStr
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()