import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _normalize_origin(origin: str) -> str:
    """Quita espacios y barras finales; ignora entradas vacías."""
    return origin.strip().rstrip("/")


def _parse_cors_allowed_origins() -> list[str]:
    """
    Orígenes CORS explícitos para desarrollo / acceso directo al backend.

    Preferir CORS_ALLOWED_ORIGINS (lista separada por comas).
    Si no está definida, se usan FRONTEND_ORIGIN y defaults locales.
    No usar '*'. Cada origen de Vercel (producción o preview) debe
    agregarse de forma explícita en Render.
    """
    raw = _get_env("CORS_ALLOWED_ORIGINS")
    if raw:
        origins: list[str] = []
        for part in raw.split(","):
            normalized = _normalize_origin(part)
            if normalized and normalized not in origins:
                origins.append(normalized)
        return origins

    origins = []
    frontend_origin = _normalize_origin(
        _get_env("FRONTEND_ORIGIN", "http://localhost:5173")
    )
    if frontend_origin:
        origins.append(frontend_origin)

    for default_origin in (
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ):
        if default_origin not in origins:
            origins.append(default_origin)

    return origins


@dataclass(frozen=True)
class Settings:
    transporte_base_url: str
    transporte_client_id: str
    transporte_client_secret: str
    frontend_origin: str
    cors_allowed_origins: list[str]


settings = Settings(
    transporte_base_url=_get_env(
        "TRANSPORTE_BASE_URL", "https://apitransporte.buenosaires.gob.ar"
    ),
    transporte_client_id=_get_env("TRANSPORTE_CLIENT_ID"),
    transporte_client_secret=_get_env("TRANSPORTE_CLIENT_SECRET"),
    frontend_origin=_get_env("FRONTEND_ORIGIN", "http://localhost:5173"),
    cors_allowed_origins=_parse_cors_allowed_origins(),
)
