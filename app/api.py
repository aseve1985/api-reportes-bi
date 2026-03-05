# main.py
from fastapi import FastAPI, Query, HTTPException, Header
import numpy as np
from .redshift import ejecutar_query_redshift
from .config import query, API_KEY


API_KEY_SGURIDAD = API_KEY

def verificar_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY_SGURIDAD:
        raise HTTPException(status_code=401, detail="Unauthorized")
    


app = FastAPI(
    title="API Reportes BI",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "API Reportes BI funcionando"}    


@app.get("/reportes/ventas")
def reporte_ventas(
    fecha_desde: str = Query(..., examples={"default": {"value": "2025-01-01"}}),
    fecha_hasta: str = Query(..., examples={"default": {"value": "2025-01-31"}}),
    x_api_key: str = Header(None)
):
    verificar_api_key(x_api_key)

    df = ejecutar_query_redshift(
        (fecha_desde, fecha_hasta)
    )

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




#python -m uvicorn app.api:app --reload --port 8000