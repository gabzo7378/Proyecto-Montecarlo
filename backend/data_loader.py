"""
============================================================================
CARGA DE DATOS GEOGRÁFICOS
Funciones para descargar y cargar datos de Natural Earth
============================================================================
"""

import geopandas as gpd
import os

URL_MAPA = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
DATA_CACHE_PATH = "data/countries.gpkg"


def cargar_datos():
    """Descarga y carga los datos de países desde Natural Earth o caché local."""
    
    # Verificar si existe caché local
    if os.path.exists(DATA_CACHE_PATH):
        try:
            print(f"Cargando datos desde caché local: {DATA_CACHE_PATH}")
            mundo = gpd.read_file(DATA_CACHE_PATH)
            print("Datos cargados correctamente desde caché!")
            return mundo
        except Exception as e:
            print(f"Error al cargar caché: {e}")
            print("Intentando descargar nuevamente...")
    
    # Descargar desde internet
    print("Descargando datos de Natural Earth...")
    print("(Esto puede tardar unos segundos la primera vez)")
    
    try:
        mundo = gpd.read_file(URL_MAPA)
        print("Datos descargados correctamente!")
        
        # Guardar en caché
        try:
            os.makedirs(os.path.dirname(DATA_CACHE_PATH), exist_ok=True)
            mundo.to_file(DATA_CACHE_PATH, driver="GPKG")
            print(f"Datos guardados en caché: {DATA_CACHE_PATH}")
        except Exception as e:
            print(f"Advertencia: No se pudo guardar caché: {e}")
        
        return mundo
    except Exception as e:
        print(f"Error al descargar: {e}")
        return None
