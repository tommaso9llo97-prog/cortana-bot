from fastapi import FastAPI
from app.routes import health, telegram, macrodroid
from app.database import engine, Base
from app.arq_worker import WorkerSettings
from arq import create_pool
import app.routes.telegram as telegram_routes

app = FastAPI(title="Cortana Assistant")

app.include_router(health.router, tags=["Health"])
app.include_router(telegram.router, prefix="/api/v1", tags=["Telegram"])
app.include_router(macrodroid.router, prefix="/api/v1", tags=["MacroDroid"])

@app.get("/")
async def root():
    return {"message": "Cortana è viva!"}

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    pool = await create_pool(WorkerSettings.redis_settings)
    telegram_routes.redis_pool = pool
    macrodroid.redis_pool = pool
    print("✅ Pronto!")