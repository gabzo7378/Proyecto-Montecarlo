"""
============================================================================
GENERADOR DE VISUALIZACIONES
Funciones para generar gráficos y visualizaciones
============================================================================
"""

import base64
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def generar_visualizacion_previa(pais_gdf, nombre_pais):
    """Genera visualización previa en coordenadas geográficas."""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    pais_gdf.plot(ax=ax, color='#667eea', edgecolor='#333333', linewidth=2, alpha=0.8)
    
    ax.set_title(f"Vista Geográfica: {nombre_pais}\n(WGS84 - Grados)", 
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("Longitud", fontsize=11)
    ax.set_ylabel("Latitud", fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.3, color='#999')
    ax.set_aspect('equal')
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_base64


def generar_visualizacion_simulacion(pais_proyectado, nombre_pais, resultados, area_real):
    """Genera visualización de la simulación Monte Carlo."""
    bbox = resultados['bbox']
    min_x, min_y, max_x, max_y = bbox
    ancho = max_x - min_x
    alto = max_y - min_y
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Dibujar el país
    pais_proyectado.plot(ax=ax, color='#667eea', edgecolor='#333333', 
                          linewidth=2, alpha=0.7, label='Área del país')
    
    # Dibujar bounding box
    rect = plt.Rectangle((min_x, min_y), ancho, alto,
                         linewidth=2, edgecolor='#ff6b6b', facecolor='none',
                         linestyle='--', label='Bounding Box')
    ax.add_patch(rect)
    
    # Dibujar puntos dentro (verde)
    if resultados['puntos_dentro_x']:
        ax.scatter(resultados['puntos_dentro_x'], resultados['puntos_dentro_y'],
                  color='#2ecc71', s=3, alpha=0.6, label=f'Puntos dentro ({len(resultados["puntos_dentro_x"]):,} muestra)')
    
    # Dibujar puntos fuera (rojo)
    if resultados['puntos_fuera_x']:
        ax.scatter(resultados['puntos_fuera_x'], resultados['puntos_fuera_y'],
                  color='#e74c3c', s=2, alpha=0.4, label=f'Puntos fuera ({len(resultados["puntos_fuera_x"]):,} muestra)')
    
    area_estimada = resultados['area_estimada_km2']
    error = abs(area_estimada - area_real) / area_real * 100 if area_real > 0 else 0
    
    ax.set_title(f"Simulación de Monte Carlo - {nombre_pais}\n"
                f"N = {resultados['n_puntos']:,} puntos | "
                f"Área estimada: {area_estimada:,.2f} km² | "
                f"Error: {error:.2f}%",
                fontsize=14, fontweight='bold')
    
    ax.set_xlabel("Coordenada X (metros)", fontsize=11)
    ax.set_ylabel("Coordenada Y (metros)", fontsize=11)
    
    # Añadir leyenda
    ax.legend(loc='upper right', fontsize=10, framealpha=0.95, 
              fancybox=True, shadow=True)
    
    ax.grid(True, alpha=0.3)
    
    ax.ticklabel_format(style='plain', axis='both')
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_base64

