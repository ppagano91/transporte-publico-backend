import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _parse_cors_allowed_origins() -> list[str]:
    """
    Orígenes CORS explícitos para desarrollo / acceso directo al backend.

    Preferir CORS_ALLOWED_ORIGINS (lista separada por comas).
    Si no está definida, se usan FRONTEND_ORIGIN y defaults locales.
    No usar '*' junto con credenciales.
    """
    raw = _get_env("CORS_ALLOWED_ORIGINS")
    if raw:
        return [origin.strip() for origin in raw.split(",") if origin.strip()]

    origins: list[str] = []
    frontend_origin = _get_env("FRONTEND_ORIGIN", "http://localhost:5173")
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
