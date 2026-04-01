from typing import Any

import httpx

from app.core.config import settings

EXTERNAL_PATH = "/colectivos/vehiclePositions"
EXTERNAL_SIMPLE_PATH = "/colectivos/vehiclePositionsSimple"
EXTERNAL_SUBTE_FORECAST_PATH = "/subtes/forecastGTFS"


class TransportApiError(Exception):
    """Base error for upstream transport API failures."""


class TransportApiTimeoutError(TransportApiError):
    """Raised when upstream request times out."""


class TransportApiHttpError(TransportApiError):
    """Raised when upstream returns non-2xx status."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


async def fetch_vehicle_positions(route_id: str = None) -> Any:
    if not settings.transporte_client_id or not settings.transporte_client_secret:
        raise TransportApiError(
            "Missing TRANSPORTE_CLIENT_ID or TRANSPORTE_CLIENT_SECRET in backend env."
        )

    params: dict[str, str] = {
        "client_id": settings.transporte_client_id,
        "client_secret": settings.transporte_client_secret,
        "json": "1",
    }

    trimmed_route_id = (route_id or "").strip()
    if trimmed_route_id:
        params["route_id"] = trimmed_route_id
    params["agency_id"] = "20"

    url = f"{settings.transporte_base_url.rstrip('/')}{EXTERNAL_PATH}"

    timeout = httpx.Timeout(10.0, connect=5.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
    except httpx.TimeoutException as exc:
        raise TransportApiTimeoutError("Timeout calling Transport API.") from exc
    except httpx.HTTPError as exc:
        raise TransportApiError("Transport API request failed.") from exc

    if response.status_code >= 400:
        text = response.text.strip()
        detail = text[:300] if text else "No detail returned by upstream API."
        raise TransportApiHttpError(
            status_code=response.status_code,
            message=f"Transport API error {response.status_code}: {detail}",
        )

    return response.json()


async def fetch_vehicle_positions_simple(
    route_id: str = None, agency_id: str = None
) -> Any:
    if not settings.transporte_client_id or not settings.transporte_client_secret:
        raise TransportApiError(
            "Missing TRANSPORTE_CLIENT_ID or TRANSPORTE_CLIENT_SECRET in backend env."
        )

    trimmed_route_id = (route_id or "").strip()
    trimmed_agency_id = (agency_id or "").strip()

    if not trimmed_route_id and not trimmed_agency_id:
        raise ValueError("At least one filter is required: route_id or agency_id.")

    params: dict[str, str] = {
        "client_id": settings.transporte_client_id,
        "client_secret": settings.transporte_client_secret,
    }

    if trimmed_route_id:
        params["route_id"] = trimmed_route_id
    if trimmed_agency_id:
        params["agency_id"] = trimmed_agency_id

    url = f"{settings.transporte_base_url.rstrip('/')}{EXTERNAL_SIMPLE_PATH}"
    timeout = httpx.Timeout(10.0, connect=5.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
    except httpx.TimeoutException as exc:
        raise TransportApiTimeoutError("Timeout calling Transport API.") from exc
    except httpx.HTTPError as exc:
        raise TransportApiError("Transport API request failed.") from exc

    if response.status_code >= 400:
        text = response.text.strip()
        detail = text[:300] if text else "No detail returned by upstream API."
        raise TransportApiHttpError(
            status_code=response.status_code,
            message=f"Transport API error {response.status_code}: {detail}",
        )

    return response.json()


async def fetch_subte_forecast() -> Any:
    if not settings.transporte_client_id or not settings.transporte_client_secret:
        raise TransportApiError(
            "Missing TRANSPORTE_CLIENT_ID or TRANSPORTE_CLIENT_SECRET in backend env."
        )

    params: dict[str, str] = {
        "client_id": settings.transporte_client_id,
        "client_secret": settings.transporte_client_secret,
    }

    url = f"{settings.transporte_base_url.rstrip('/')}{EXTERNAL_SUBTE_FORECAST_PATH}"
    timeout = httpx.Timeout(10.0, connect=5.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
    except httpx.TimeoutException as exc:
        raise TransportApiTimeoutError("Timeout calling Transport API.") from exc
    except httpx.HTTPError as exc:
        raise TransportApiError("Transport API request failed.") from exc

    if response.status_code >= 400:
        text = response.text.strip()
        detail = text[:300] if text else "No detail returned by upstream API."
        raise TransportApiHttpError(
            status_code=response.status_code,
            message=f"Transport API error {response.status_code}: {detail}",
        )

    return response.json()
