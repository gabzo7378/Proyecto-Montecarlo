"""
============================================================================
CONFIGURACIÓN DEL PROYECTO
Constantes y configuraciones globales
============================================================================
"""

# Lista de países de Sudamérica (nombres en inglés como aparecen en Natural Earth)
PAISES_SUDAMERICA = [
    "Argentina",
    "Bolivia",
    "Brazil",
    "Chile",
    "Colombia",
    "Ecuador",
    "Guyana",
    "Paraguay",
    "Peru",
    "Suriname",
    "Uruguay",
    "Venezuela"
]

# Áreas reales de referencia en km² (Fuente: Banco Mundial / Wikipedia)
AREAS_REALES_KM2 = {
    "Argentina": 2780400,
    "Bolivia": 1098581,
    "Brazil": 8515770,
    "Chile": 756102,
    "Colombia": 1138910,
    "Ecuador": 283561,
    "Guyana": 214969,
    "Paraguay": 406752,
    "Peru": 1285216,
    "Suriname": 165940,
    "Uruguay": 176215,
    "Venezuela": 916445
}

# URL de datos geográficos
URL_MAPA = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

# Configuración de proyección
PROYECCION_PRINCIPAL = "ESRI:102033"
PROYECCION_ALTERNATIVA = "EPSG:32718"

# Configuración de caché
DATA_CACHE_PATH = "data/countries.gpkg"

# Configuración de visualización
# MAX_PUNTOS_VIZ = 50000 # para limitar el número de puntos visibles
MAX_PUNTOS_VIZ = float('inf') # para deshabilitar el límite
