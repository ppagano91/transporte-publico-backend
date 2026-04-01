from fastapi import APIRouter, HTTPException, Query

from app.services.ecobici_api import (
    EcobiciApiError,
    EcobiciApiHttpError,
    EcobiciApiTimeoutError,
    fetch_station_information,
    fetch_station_status,
)

router = APIRouter()


@router.get("/api/ecobici/station-information")
async def get_station_information(
    force_refresh: bool = Query(
        default=False,
        description="Bypass in-memory cache and fetch fresh station information.",
    ),
):
    try:
        payload = await fetch_station_information(force_refresh=force_refresh)
        return payload
    except EcobiciApiTimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="Timeout while querying external Ecobici API.",
        ) from exc
    except EcobiciApiHttpError as exc:
        raise HTTPException(
            status_code=502,
            detail=exc.message,
        ) from exc
    except EcobiciApiError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc) or "Unexpected backend Ecobici error.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error while fetching station information.",
        ) from exc


@router.get("/api/ecobici/station-status")
async def get_station_status():
    try:
        payload = await fetch_station_status()
        return payload
    except EcobiciApiTimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="Timeout while querying external Ecobici API.",
        ) from exc
    except EcobiciApiHttpError as exc:
        raise HTTPException(
            status_code=502,
            detail=exc.message,
        ) from exc
    except EcobiciApiError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc) or "Unexpected backend Ecobici error.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error while fetching station status.",
        ) from exc
