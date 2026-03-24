from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.collector_service import CollectorService
from app.core.database import AsyncSessionLocal

scheduler = AsyncIOScheduler()

async def scheduled_collection():
    async with AsyncSessionLocal() as db:
        service = CollectorService()
        await service.run_collection_for_all_active_products(db)

def start_scheduler():
    # Executa a cada 5 minutos (ajustável)
    scheduler.add_job(scheduled_collection, 'interval', minutes=5)
    scheduler.start()

def shutdown_scheduler():
    scheduler.shutdown()