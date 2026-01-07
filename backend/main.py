"""
============================================================================
APLICACIÓN PRINCIPAL
FastAPI Backend para Calculador de Área Monte Carlo
============================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data_loader import cargar_datos
from routes import router, set_mundo

app = FastAPI(title="Monte Carlo Area Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Cargar datos geográficos al iniciar la aplicación."""
    mundo = cargar_datos()
    if mundo is None:
        print("ERROR: No se pudieron cargar los datos geográficos")
    else:
        set_mundo(mundo)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

