from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.scheduler import start_scheduler, shutdown_scheduler

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Inclui as rotas da API versão 1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Monitor de Preços API"}

@app.on_event("startup")
async def startup_event():
    start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    shutdown_scheduler()