import asyncio
from arq import Worker
from app.arq_worker import WorkerSettings

if __name__ == "__main__":
    worker = Worker(WorkerSettings)
    asyncio.run(worker.run())