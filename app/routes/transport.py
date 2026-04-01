from fastapi import APIRouter, HTTPException, Query

from app.services.transport_api import (
    TransportApiError,
    TransportApiHttpError,
    TransportApiTimeoutError,
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
