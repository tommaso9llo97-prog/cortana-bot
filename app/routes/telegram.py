import uuid
from fastapi import APIRouter, Request, Depends, HTTPException
from app.security import verify_telegram_secret, is_telegram_user_allowed

router = APIRouter()
redis_pool = None

@router.post("/telegram/webhook")
async def telegram_webhook(request: Request, _: bool = Depends(verify_telegram_secret)):
    global redis_pool
    data = await request.json()
    payload_src = data.get("message") or data.get("edited_message") or data.get("callback_query", {}).get("message") or {}
    from_user = payload_src.get("from") or data.get("callback_query", {}).get("from") or {}
    user_id = str(from_user.get("id", ""))
    text = payload_src.get("text", "")

    if not user_id or not is_telegram_user_allowed(user_id):
        return {"status": "ignored"}

    if not text:
        return {"status": "ignored", "reason": "empty"}

    event_uuid = str(uuid.uuid4())
    if redis_pool:
        job = await redis_pool.enqueue_job("process_telegram_message", user_id, text, event_uuid)
        return {"status": "accepted", "job_id": job.job_id}
    else:
        raise HTTPException(status_code=503, detail="Worker non disponibile")