from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.core.config import settings


class GtfsShapesError(Exception):
    """Base error for GTFS shapes data access."""


def _trim_or_none(value: str | None) -> str | None:
    trimmed = (value or "").strip()
    return trimmed or None


def fetch_unique_shapes(route_id: str | None = None, agency_id: str | None = None) -> list[dict[str, Any]]:
    trimmed_route_id = _trim_or_none(route_id)
    trimmed_agency_id = _trim_or_none(agency_id)

    query = """
        SELECT DISTINCT ON (shape_id)
            route_id,
            agency_id,
            route_short_name,
            route_long_name,
            direction_id,
            shape_id,
            ST_AsGeoJSON(geom)::json AS geometry
        FROM gtfs.v_routes_geoms
        WHERE geom IS NOT NULL
          AND (%(route_id)s::text IS NULL OR route_id = %(route_id)s::text)
          AND (%(agency_id)s::text IS NULL OR agency_id = %(agency_id)s::text)
        ORDER BY shape_id, route_id, direction_id
    """

    try:
        with psycopg.connect(settings.gtfs_db_dsn, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    {"route_id": trimmed_route_id, "agency_id": trimmed_agency_id},
                )
                rows = cur.fetchall()
    except psycopg.Error as exc:
        raise GtfsShapesError("Error querying GTFS shapes from database.") from exc

    return [dict(row) for row in rows]
