from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
NETWORK_FILE = DATA_DIR / "red_subte.json"
STATIONS_FILE = DATA_DIR / "estaciones_de_subte.json"

_network_cache: dict[str, Any] | None = None
_stations_cache: dict[str, Any] | None = None


class SubteStaticDataError(Exception):
    """Base error for static subway geometry data."""


class SubteStaticFileNotFoundError(SubteStaticDataError):
    """Raised when a static GeoJSON file is missing."""


class SubteStaticInvalidJsonError(SubteStaticDataError):
    """Raised when a static file is not valid JSON/GeoJSON."""


def _load_geojson(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SubteStaticFileNotFoundError(
            f"Archivo estatico de subtes no encontrado: {path.name}"
        )

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        raise SubteStaticInvalidJsonError(
            f"No se pudo leer el archivo estatico de subtes: {path.name}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise SubteStaticInvalidJsonError(
            f"JSON invalido en archivo estatico de subtes: {path.name}"
        ) from exc

    if not isinstance(payload, dict):
        raise SubteStaticInvalidJsonError(
            f"El archivo estatico de subtes no es un objeto JSON: {path.name}"
        )

    if payload.get("type") != "FeatureCollection":
        raise SubteStaticInvalidJsonError(
            f"Se esperaba un FeatureCollection en: {path.name}"
        )

    features = payload.get("features")
    if not isinstance(features, list):
        raise SubteStaticInvalidJsonError(
            f"FeatureCollection sin features validas en: {path.name}"
        )

    return payload


def get_subte_network(*, force_refresh: bool = False) -> dict[str, Any]:
    global _network_cache

    if force_refresh or _network_cache is None:
        _network_cache = _load_geojson(NETWORK_FILE)

    return _network_cache


def get_subte_stations(*, force_refresh: bool = False) -> dict[str, Any]:
    global _stations_cache

    if force_refresh or _stations_cache is None:
        _stations_cache = _load_geojson(STATIONS_FILE)

    return _stations_cache
