from typing import Any

import httpx

from app.core.config import settings

EXTERNAL_STATION_INFORMATION_PATH = "/ecobici/gbfs/stationInformation"
EXTERNAL_STATION_STATUS_PATH = "/ecobici/gbfs/stationStatus"

_station_information_cache: Any  = None


class EcobiciApiError(Exception):
    """Base error for upstream Ecobici API failures."""


class EcobiciApiTimeoutError(EcobiciApiError):
    """Raised when upstream request times out."""


class EcobiciApiHttpError(EcobiciApiError):
    """Raised when upstream returns non-2xx status."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def _build_base_params() -> dict[str, str]:
    if not settings.transporte_client_id or not settings.transporte_client_secret:
        raise EcobiciApiError(
            "Missing TRANSPORTE_CLIENT_ID or TRANSPORTE_CLIENT_SECRET in backend env."
        )

    return {
        "client_id": settings.transporte_client_id,
        "client_secret": settings.transporte_client_secret,
    }


async def _fetch_json(path: str) -> Any:
    url = f"{settings.transporte_base_url.rstrip('/')}{path}"
    params = _build_base_params()
    timeout = httpx.Timeout(10.0, connect=5.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
    except httpx.TimeoutException as exc:
        raise EcobiciApiTimeoutError("Timeout calling Ecobici API.") from exc
    except httpx.HTTPError as exc:
        raise EcobiciApiError("Ecobici API request failed.") from exc

    if response.status_code >= 400:
        text = response.text.strip()
        detail = text[:300] if text else "No detail returned by upstream API."
        raise EcobiciApiHttpError(
            status_code=response.status_code,
            message=f"Ecobici API error {response.status_code}: {detail}",
        )

    return response.json()


async def fetch_station_information(force_refresh: bool = False) -> Any:
    global _station_information_cache

    if _station_information_cache is not None and not force_refresh:
        return _station_information_cache

    payload = await _fetch_json(EXTERNAL_STATION_INFORMATION_PATH)
    _station_information_cache = payload
    return payload


async def fetch_station_status() -> Any:
    return await _fetch_json(EXTERNAL_STATION_STATUS_PATH)
