from arq import create_pool
from app.worker import process_telegram_message, process_macrodroid_event
from app.config import settings
import logging

logger = logging.getLogger(__name__)

async def startup(ctx):
    ctx['redis'] = await create_pool(settings.REDIS_URL)
    logger.info("Worker avviato.")

async def shutdown(ctx):
    await ctx['redis'].close()

class WorkerSettings:
    functions = [process_telegram_message, process_macrodroid_event]
    redis_settings = settings.redis_settings
    on_startup = startup
    on_shutdown = shutdown
    max_jobs = 10
    job_timeout = 60
    retry_jobs = True
    max_retries = 3
    retry_backoff = 5