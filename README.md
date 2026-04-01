# Backend proxy (FastAPI)

Backend minimo para evitar CORS y ocultar credenciales de Transporte GCBA.

## Requisitos

- Python 3.10+

## Setup

```bash
cd backend
python -m venv .venv
```

Activar el entorno virtual:

- Windows PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- Linux/macOS:
  ```bash
  source .venv/bin/activate
  ```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Crear variables de entorno:

```bash
cp .env.example .env
```

Editar `.env` con `TRANSPORTE_CLIENT_ID` y `TRANSPORTE_CLIENT_SECRET`.

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `GET /health`
- `GET /api/vehicle-positions`
  - query opcional: `route_id`
- `GET /api/vehicle-positions-simple`
  - query opcionales: `route_id`, `agency_id`
  - requiere al menos uno de los dos filtros
- `GET /api/subtes/forecast`
  - proxy de `GET /subtes/forecastGTFS`
  - no requiere coordenadas ni filtros adicionales
- `GET /api/ecobici/station-information`
  - proxy de `GET /ecobici/gbfs/stationInformation`
  - query opcional: `force_refresh` (default `false`) para invalidar cache en memoria
- `GET /api/ecobici/station-status`
  - proxy de `GET /ecobici/gbfs/stationStatus`
