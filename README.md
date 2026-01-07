# Calculador de Área con Método de Monte Carlo

Aplicación web para estimar áreas territoriales de países sudamericanos usando el método de Monte Carlo.

## Estructura del Proyecto

```
area_montecarlo/
├── backend/           # API FastAPI
│   ├── main.py       # Servidor principal
│   ├── config.py     # Configuración
│   ├── data_loader.py
│   ├── geometry_processor.py
│   ├── montecarlo_simulator.py
│   ├── requirements.txt
│   └── data/         # Caché de datos geográficos
└── frontend/         # Interfaz web
    ├── index.html
    ├── styles.css
    └── script.js
```

## Instalación

### Backend

1. Crear entorno virtual:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar servidor:

```bash
python main.py
```

El servidor estará disponible en `http://localhost:8000`

### Frontend

Abrir `frontend/index.html` en un navegador web moderno.

## Uso

1. Iniciar el backend
2. Abrir el frontend en el navegador
3. Seleccionar un país
4. Elegir cantidad de puntos (recomendado: 100,000)
5. Hacer clic en "Calcular Área"
6. Ver resultados y visualización

## Características

- **Caché local**: Los datos geográficos se guardan localmente para uso sin internet
- **Interfaz moderna**: Diseño responsivo con gradientes y animaciones
- **Resultados completos**: Estadísticas, error relativo y visualización gráfica
- **API REST**: Backend FastAPI con documentación automática en `/docs`
