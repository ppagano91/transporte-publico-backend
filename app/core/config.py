import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    transporte_base_url: str
    transporte_client_id: str
    transporte_client_secret: str
    frontend_origin: str


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


settings = Settings(
    transporte_base_url=_get_env(
        "TRANSPORTE_BASE_URL", "https://apitransporte.buenosaires.gob.ar"
    ),
    transporte_client_id=_get_env("TRANSPORTE_CLIENT_ID"),
    transporte_client_secret=_get_env("TRANSPORTE_CLIENT_SECRET"),
    frontend_origin=_get_env("FRONTEND_ORIGIN", "http://localhost:5173"),
)
