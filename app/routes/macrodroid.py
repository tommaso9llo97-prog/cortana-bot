from fastapi import APIRouter, Request, Depends, HTTPException
from app.security import verify_macrodroid_key
from app.idempotency import generate_macrodroid_idempotency_key
from app.routes.telegram import redis_pool

router = APIRouter()

@router.post("/macrodroid/event", status_code=202)
async def macrodroid_event(request: Request, _: bool = Depends(verify_macrodroid_key)):
    global redis_pool
    data = await request.json()
    telegram_id = data.get("telegram_id")
    event_type = data.get("event")
    payload = data.get("payload", {})

    if not telegram_id or not event_type:
        raise HTTPException(status_code=400, detail="Missing fields")

    idem_key = generate_macrodroid_idempotency_key(telegram_id, event_type, payload)

    if redis_pool:
        redis_key = f"idem:{idem_key}"
        if not await redis_pool.set(redis_key, "1", ex=120, nx=True):
            return {"status": "duplicate"}

        job = await redis_pool.enqueue_job("process_macrodroid_event", telegram_id, event_type, payload, idem_key)
        return {"status": "accepted", "job_id": job.job_id}
    else:
        raise HTTPException(status_code=503, detail="Worker non disponibile")