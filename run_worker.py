import asyncio
from arq import run_worker
from app.arq_worker import WorkerSettings

if __name__ == '__main__':
    # Usiamo direttamente l'inizializzatore nativo di arq per evitare conflitti di tipi con Python 3.13
    asyncio.run(run_worker(WorkerSettings))