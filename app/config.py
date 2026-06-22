from pydantic_settings import BaseSettings
from pydantic import SecretStr
from arq.connections import RedisSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:////assistant.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    WEBHOOK_SECRET: SecretStr
    MACRODROID_API_KEY: SecretStr
    ALLOWED_TELEGRAM_IDS: str
    TELEGRAM_BOT_TOKEN: SecretStr
    GEMINI_API_KEY: SecretStr

    @property
    def redis_settings(self) -> RedisSettings:
        # Questo converte automaticamente la stringa nell'oggetto che Arq pretende!
        return RedisSettings.from_dsn(self.REDIS_URL)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()