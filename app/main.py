from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes.ecobici import router as ecobici_router
from app.routes.transport import router as transport_router

app = FastAPI(title="Demo Transporte Backend", version="0.1.0")

# Orígenes explícitos vía CORS_ALLOWED_ORIGINS (coma-separados).
# Desarrollo con proxy de Vite: same-origin en :5173, CORS no interviene.
# Producción (Vercel → Render): agregar el dominio del frontend en Render.
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
