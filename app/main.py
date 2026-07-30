from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes.ecobici import router as ecobici_router
from app.routes.transport import router as transport_router

app = FastAPI(title="Demo Transporte Backend", version="0.1.0")

# Orígenes explícitos (ver CORS_ALLOWED_ORIGINS). Con el proxy de Vite el
# navegador habla same-origin con :5173 y no necesita CORS; esto cubre el
# acceso directo al backend en desarrollo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "message": "API de Subtes de la Ciudad Autónoma de Buenos Aires"
        }


app.include_router(transport_router)
app.include_router(ecobici_router)
