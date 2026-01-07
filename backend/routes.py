from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config import PAISES_SUDAMERICA, AREAS_REALES_KM2
from data_loader import cargar_datos
from geometry_processor import proyectar_y_calcular_bbox
from montecarlo_simulator import simulacion_montecarlo
from display import generar_visualizacion_previa, generar_visualizacion_simulacion

router = APIRouter()

# Variable global para datos
mundo = None


def set_mundo(data):
    """Establece los datos geográficos cargados."""
    global mundo
    mundo = data


class SimulacionRequest(BaseModel):
    pais: str
    n_puntos: int


@router.get("/")
def root():
    return {"message": "Monte Carlo Area Calculator API"}


@router.get("/paises")
def get_paises():
    """Retorna lista de países disponibles."""
    return {
        "paises": [
            {
                "nombre": pais,
                "area_real": AREAS_REALES_KM2.get(pais, 0)
            }
            for pais in PAISES_SUDAMERICA
        ]
    }


@router.post("/simular")
def simular(request: SimulacionRequest):
    """Ejecuta la simulación de Monte Carlo."""
    global mundo
    
    if mundo is None:
        raise HTTPException(status_code=500, detail="Datos geográficos no disponibles")
    
    if request.pais not in PAISES_SUDAMERICA:
        raise HTTPException(status_code=400, detail="País no válido")
    
    if request.n_puntos < 100 or request.n_puntos > 10_000_000:
        raise HTTPException(status_code=400, detail="Cantidad de puntos fuera de rango (100-10,000,000)")
    
    # Filtrar país
    pais_gdf = mundo[mundo['NAME'] == request.pais]
    
    if pais_gdf.empty:
        raise HTTPException(status_code=404, detail=f"País '{request.pais}' no encontrado")
    
    # Procesar geometría
    geo_info = proyectar_y_calcular_bbox(pais_gdf, request.pais)
    
    # Ejecutar simulación
    resultados = simulacion_montecarlo(
        geo_info['pais_proyectado'],
        geo_info['bbox'],
        request.n_puntos
    )
    
    # Calcular error
    area_real = AREAS_REALES_KM2.get(request.pais, 0)
    area_estimada = resultados['area_estimada_km2']
    
    if area_real > 0:
        error_absoluto = abs(area_estimada - area_real)
        error_relativo = (error_absoluto / area_real) * 100
    else:
        error_absoluto = 0
        error_relativo = 0
    
    # Generar visualizaciones
    imagen_previa = generar_visualizacion_previa(pais_gdf, request.pais)
    imagen_simulacion = generar_visualizacion_simulacion(
        geo_info['pais_proyectado'],
        request.pais,
        resultados,
        area_real
    )
    
    return {
        "pais": request.pais,
        "area_real_km2": area_real,
        "coordenadas_geograficas": geo_info['coords_geo'],
        "coordenadas_proyectadas": geo_info['coords_proyectadas'],
        "proyeccion": geo_info['proyeccion'],
        "simulacion": {
            "n_puntos": resultados['n_puntos'],
            "puntos_dentro": resultados['puntos_dentro'],
            "puntos_fuera": resultados['puntos_fuera'],
            "tiempo_segundos": round(resultados['tiempo_simulacion'], 2),
            "area_bbox_km2": round(resultados['area_bbox_m2'] / 1_000_000, 2),
            "proporcion": round(resultados['puntos_dentro'] / resultados['n_puntos'], 6),
            "area_estimada_km2": round(area_estimada, 2)
        },
        "validacion": {
            "area_real_km2": area_real,
            "area_estimada_km2": round(area_estimada, 2),
            "error_absoluto_km2": round(error_absoluto, 2),
            "error_relativo_porcentaje": round(error_relativo, 4)
        },
        "visualizacion_previa": imagen_previa,
        "visualizacion_simulacion": imagen_simulacion
    }
