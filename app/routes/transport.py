from typing import NoReturn

from fastapi import APIRouter, HTTPException, Query

from app.services.subte_static import (
    SubteStaticDataError,
    SubteStaticFileNotFoundError,
    SubteStaticInvalidJsonError,
    get_subte_network,
    get_subte_stations,
)
from app.services.transport_api import (
    TransportApiError,
    TransportApiHttpError,
    TransportApiTimeoutError,
    fetch_semaforos,
    fetch_subte_forecast,
    fetch_vehicle_positions,
    fetch_vehicle_positions_simple,
)

router = APIRouter()


@router.get("/api/vehicle-positions")
async def get_vehicle_positions(
    route_id: str = Query(default="", description="Optional route id")
):
    try:
        payload = await fetch_vehicle_positions(route_id=route_id)
        return payload
    except TransportApiTimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="Timeout while querying external Transport API.",
        ) from exc
    except TransportApiHttpError as exc:
        raise HTTPException(
            status_code=502,
            detail=exc.message,
        ) from exc
    except TransportApiError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc) or "Unexpected backend transport error.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error while fetching vehicle positions.",
        ) from exc


@router.get("/api/vehicle-positions-simple")
async def get_vehicle_positions_simple(
    route_id: str = Query(default="", description="Optional route id"),
    agency_id: str = Query(default="", description="Optional agency id"),
):
    try:
        payload = await fetch_vehicle_positions_simple(
            route_id=route_id, agency_id=agency_id
        )
        return payload
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TransportApiTimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="Timeout while querying external Transport API.",
        ) from exc
    except TransportApiHttpError as exc:
        raise HTTPException(
            status_code=502,
            detail=exc.message,
        ) from exc
    except TransportApiError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc) or "Unexpected backend transport error.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error while fetching vehicle positions simple.",
        ) from exc


@router.get("/api/subtes/forecast")
async def get_subte_forecast():
    try:
        payload = await fetch_subte_forecast()
        return payload
    except TransportApiTimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="Timeout while querying external Transport API.",
        ) from exc
    except TransportApiHttpError as exc:
        raise HTTPException(
            status_code=502,
            detail=exc.message,
        ) from exc
    except TransportApiError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc) or "Unexpected backend transport error.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error while fetching subte forecast.",
        ) from exc


def _raise_subte_static_http_error(exc: Exception) -> NoReturn:
    if isinstance(exc, SubteStaticFileNotFoundError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, SubteStaticInvalidJsonError):
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    if isinstance(exc, SubteStaticDataError):
        raise HTTPException(
            status_code=500,
            detail=str(exc) or "Error al leer datos estaticos de subtes.",
        ) from exc
    raise HTTPException(
        status_code=500,
        detail="Unexpected server error while loading static subway data.",
    ) from exc


@router.get("/api/subtes/network")
async def get_subte_network_geojson(
    force_refresh: bool = Query(
        default=False,
        description="Bypass in-memory cache and reload network GeoJSON from disk.",
    ),
):
    try:
        return get_subte_network(force_refresh=force_refresh)
    except Exception as exc:
        _raise_subte_static_http_error(exc)


@router.get("/api/subtes/stations")
async def get_subte_stations_geojson(
    force_refresh: bool = Query(
        default=False,
        description="Bypass in-memory cache and reload stations GeoJSON from disk.",
    ),
):
    try:
        return get_subte_stations(force_refresh=force_refresh)
    except Exception as exc:
        _raise_subte_static_http_error(exc)


@router.get("/api/transito/semaforos")
async def get_semaforos():
    try:
        payload = await fetch_semaforos()
        return payload
    except TransportApiTimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="Timeout while querying external Transport API.",
        ) from exc
    except TransportApiHttpError as exc:
        raise HTTPException(
            status_code=502,
            detail=exc.message,
        ) from exc
    except TransportApiError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc) or "Unexpected backend transport error.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error while fetching semaforos.",
        ) from exc
