import logging
from sqlalchemy.exc import IntegrityError
from app.database import AsyncSessionLocal
from app.models import User, DeviceEvent, DeviceEventType, Conversation, ConversationRole
from app.gemini import get_gemini_response
from app.config import settings
from app.security import get_allowed_users
import httpx

logger = logging.getLogger(__name__)

async def process_telegram_message(ctx, user_id, text, event_uuid):
    async with AsyncSessionLocal() as db:
        from sqlalchemy.future import select
        result = await db.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            is_owner = user_id in get_allowed_users()
            user = User(telegram_id=user_id, is_owner=is_owner)
            db.add(user)
            await db.commit()
            await db.refresh(user)

        reply = await get_gemini_response(user.id, text, ctx.get('redis'))

        db.add(Conversation(user_id=user.id, role=ConversationRole.USER, content=text))
        db.add(Conversation(user_id=user.id, role=ConversationRole.ASSISTANT, content=reply))
        await db.commit()

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(url, json={"chat_id": user_id, "text": reply})

    return {"status": "processed"}

async def process_macrodroid_event(ctx, telegram_id, event_type, payload, idem_key):
    async with AsyncSessionLocal() as db:
        from sqlalchemy.future import select
        result = await db.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            logger.warning(f"Utente {telegram_id} non registrato.")
            return {"status": "ignored"}

        try:
            evt_type = DeviceEventType(event_type)
        except ValueError:
            logger.error(f"Tipo evento sconosciuto: {event_type}")
            return {"status": "error"}

        new_event = DeviceEvent(
            user_id=user.id,
            event_type=evt_type,
            payload=payload,
            idempotency_key=idem_key
        )
        db.add(new_event)

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            logger.info(f"Evento {idem_key} già processato.")
            return {"status": "duplicate"}

        if evt_type == DeviceEventType.APP_USAGE and payload.get('app', '').lower() == 'youtube':
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}/sendMessage"
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(url, json={
                    "chat_id": telegram_id,
                    "text": "🚨 Hai aperto YouTube! Torna al lavoro."
                })

    return {"status": "processed"}