"""
============================================================================
PROCESAMIENTO DE GEOMETRÍA
Funciones para proyectar y calcular bounding box
============================================================================
"""

from config import PROYECCION_PRINCIPAL, PROYECCION_ALTERNATIVA


def proyectar_y_calcular_bbox(pais_gdf, nombre_pais):
    """
    Proyecta el país a sistema métrico y calcula el bounding box.
    
    Returns:
        dict con información de proyección y bbox
    """
    bounds_geo = pais_gdf.total_bounds
    min_lon, min_lat, max_lon, max_lat = bounds_geo
    
    try:
        pais_proyectado = pais_gdf.to_crs(PROYECCION_PRINCIPAL)
        proyeccion_usada = PROYECCION_PRINCIPAL
    except:
        pais_proyectado = pais_gdf.to_crs(PROYECCION_ALTERNATIVA)
        proyeccion_usada = PROYECCION_ALTERNATIVA
    
    min_x, min_y, max_x, max_y = pais_proyectado.total_bounds
    
    ancho = max_x - min_x
    alto = max_y - min_y
    area_bbox = ancho * alto
    
    return {
        'pais_proyectado': pais_proyectado,
        'bbox': (min_x, min_y, max_x, max_y),
        'coords_geo': {
            'min_lat': min_lat,
            'max_lat': max_lat,
            'min_lon': min_lon,
            'max_lon': max_lon
        },
        'coords_proyectadas': {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'ancho': ancho,
            'alto': alto,
            'area_bbox_m2': area_bbox,
            'area_bbox_km2': area_bbox / 1_000_000
        },
        'proyeccion': proyeccion_usada
    }
