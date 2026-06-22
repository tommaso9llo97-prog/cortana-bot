from fastapi import Header, HTTPException, Security
from fastapi.security import APIKeyHeader
from app.config import settings

X_API_KEY = APIKeyHeader(name="X-API-KEY", auto_error=False)

def get_allowed_users():
    return {uid.strip() for uid in settings.ALLOWED_TELEGRAM_IDS.split(",") if uid.strip()}

def verify_macrodroid_key(api_key: str = Security(X_API_KEY)):
    if not api_key or api_key != settings.MACRODROID_API_KEY.get_secret_value():
        raise HTTPException(status_code=401, detail="Chiave non valida.")
    return api_key

def verify_telegram_secret(telegram_secret: str = Header(None, alias="X-Telegram-Bot-Api-Secret-Token")):
    if not telegram_secret or telegram_secret != settings.WEBHOOK_SECRET.get_secret_value():
        raise HTTPException(status_code=403, detail="Non autorizzato.")
    return telegram_secret

def is_telegram_user_allowed(telegram_id: str) -> bool:
    return telegram_id in get_allowed_users()