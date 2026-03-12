# main.py
from fastapi import FastAPI, Query, HTTPException, Header
import numpy as np
from .redshift import ejecutar_query_redshift
from .config import query, API_KEY

from pydantic import BaseModel
from typing import List, Dict, Any

from fastapi.middleware.cors import CORSMiddleware

import httpx


class ReporteVentasResponse(BaseModel):
    status: str
    rows: int
    data: List[Dict[str, Any]]


API_KEY_SGURIDAD = API_KEY

def verificar_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY_SGURIDAD:
        raise HTTPException(status_code=401, detail="Unauthorized")
    


app = FastAPI(
    title="API Reportes BI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "API Reportes BI funcionando"}    


@app.get("/reportes/ventas", response_model=ReporteVentasResponse)
def reporte_ventas(
    fecha_desde: str = Query(..., example="2025-01-01"),
    fecha_hasta: str = Query(..., example="2025-01-31"),
    x_api_key: str = Header(None)
):
    verificar_api_key(x_api_key)

    df = ejecutar_query_redshift((fecha_desde, fecha_hasta))

    df = df.replace({np.nan: None})

    if df is None or df.empty:
        return {
            "status": "ok",
            "rows": 0,
            "data": []
        }

    return {
        "status": "ok",
        "rows": len(df),
        "data": df.to_dict(orient="records")
    }


@app.get("/proxy/ventas")
async def proxy_ventas(
    fecha_desde: str = Query(..., example="2025-01-01"),
    fecha_hasta: str = Query(..., example="2025-01-31")
):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://api-reportes-bi.onrender.com/reportes/ventas",
            params={"fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta},
            headers={"x-api-key": API_KEY_SGURIDAD}
        )
        return r.json()




#python -m uvicorn app.api:app --reload --port 8000