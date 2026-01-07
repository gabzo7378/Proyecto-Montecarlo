"""
============================================================================
SIMULADOR DE MONTE CARLO
Funciones para ejecutar la simulación de Monte Carlo
============================================================================
"""

import numpy as np
from shapely.geometry import Point
import time
from config import MAX_PUNTOS_VIZ


def simulacion_montecarlo(pais_proyectado, bbox, n_puntos):
    """
    Ejecuta la simulación de Monte Carlo para estimar el área.
    
    Args:
        pais_proyectado: GeoDataFrame con el polígono proyectado
        bbox: tupla (min_x, min_y, max_x, max_y)
        n_puntos: cantidad de puntos pseudoaleatorios a generar
    
    Returns:
        dict con resultados de la simulación
    """
    min_x, min_y, max_x, max_y = bbox
    
    ancho = max_x - min_x
    alto = max_y - min_y
    area_bbox = ancho * alto
    
    start_time = time.time()
    
    # Generar puntos aleatorios con distribución uniforme
    x_rand = np.random.uniform(min_x, max_x, n_puntos)
    y_rand = np.random.uniform(min_y, max_y, n_puntos)
    
    poligono_pais = pais_proyectado.geometry.iloc[0]
    
    puntos_dentro = 0
    puntos_dentro_x = []
    puntos_dentro_y = []
    puntos_fuera_x = []
    puntos_fuera_y = []
    
    max_puntos_viz = min(MAX_PUNTOS_VIZ, n_puntos)
    
    for x, y in zip(x_rand, y_rand):
        punto = Point(x, y)
        if poligono_pais.contains(punto):
            puntos_dentro += 1
            if len(puntos_dentro_x) < max_puntos_viz:
                puntos_dentro_x.append(x)
                puntos_dentro_y.append(y)
        else:
            if len(puntos_fuera_x) < max_puntos_viz // 2:
                puntos_fuera_x.append(x)
                puntos_fuera_y.append(y)
    
    end_time = time.time()
    tiempo_simulacion = end_time - start_time
    
    # Calcular área estimada con Monte Carlo
    # Fórmula: Área_Estimada = Área_BBox × (puntos_dentro / total_puntos)
    area_estimada_m2 = area_bbox * (puntos_dentro / n_puntos)
    area_estimada_km2 = area_estimada_m2 / 1_000_000
    
    return {
        'n_puntos': n_puntos,
        'puntos_dentro': puntos_dentro,
        'puntos_fuera': n_puntos - puntos_dentro,
        'area_bbox_m2': area_bbox,
        'area_estimada_m2': area_estimada_m2,
        'area_estimada_km2': area_estimada_km2,
        'tiempo_simulacion': tiempo_simulacion,
        'puntos_dentro_x': puntos_dentro_x,
        'puntos_dentro_y': puntos_dentro_y,
        'puntos_fuera_x': puntos_fuera_x,
        'puntos_fuera_y': puntos_fuera_y,
        'bbox': bbox
    }
