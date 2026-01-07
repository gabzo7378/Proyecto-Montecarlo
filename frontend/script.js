const API_URL = "https://montecarlo-backend-production.up.railway.app";
// Cargar países al inicio
document.addEventListener("DOMContentLoaded", async () => {
  await cargarPaises();

  document
    .getElementById("simular-btn")
    .addEventListener("click", ejecutarSimulacion);
});

async function cargarPaises() {
  try {
    const response = await fetch(`${API_URL}/paises`);
    const data = await response.json();

    const select = document.getElementById("pais-select");
    select.innerHTML = '<option value="">Seleccione un país...</option>';

    data.paises.forEach((pais) => {
      const option = document.createElement("option");
      option.value = pais.nombre;
      option.textContent = `${pais.nombre
        } (Área real: ${pais.area_real.toLocaleString()} km²)`;
      select.appendChild(option);
    });
  } catch (error) {
    console.error("Error al cargar países:", error);
    alert(
      "Error al conectar con el servidor. Asegúrese de que el backend esté ejecutándose."
    );
  }
}

async function ejecutarSimulacion() {
  const pais = document.getElementById("pais-select").value;
  const nPuntos = parseInt(document.getElementById("n-puntos").value);

  if (!pais) {
    alert("Por favor seleccione un país");
    return;
  }

  if (nPuntos < 100 || nPuntos > 10000000) {
    alert("La cantidad de puntos debe estar entre 100 y 10,000,000");
    return;
  }

  // Mostrar loading
  document.getElementById("loading").classList.remove("hidden");
  document.getElementById("resultados").classList.add("hidden");
  document.getElementById("simular-btn").disabled = true;

  try {
    const response = await fetch(`${API_URL}/simular`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        pais: pais,
        n_puntos: nPuntos,
      }),
    });

    if (!response.ok) {
      throw new Error("Error en la simulación");
    }

    const data = await response.json();
    mostrarResultados(data);
  } catch (error) {
    console.error("Error:", error);
    alert("Error al ejecutar la simulación. Por favor intente nuevamente.");
  } finally {
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("simular-btn").disabled = false;
  }
}

function mostrarResultados(data) {
  // Actualizar tarjetas principales
  document.getElementById("pais-nombre").textContent = data.pais;
  document.getElementById(
    "area-real"
  ).textContent = `${data.area_real_km2.toLocaleString()} km²`;
  document.getElementById(
    "area-estimada"
  ).textContent = `${data.simulacion.area_estimada_km2.toLocaleString()} km²`;

  // Error relativo con color según evaluación
  const errorClass =
    data.validacion.evaluacion === "excelente"
      ? "success"
      : data.validacion.evaluacion === "buena"
        ? "warning"
        : data.validacion.evaluacion === "aceptable"
          ? "moderate"
          : "error";
  document.getElementById(
    "error-relativo"
  ).textContent = `${data.validacion.error_relativo_porcentaje}%`;
  document.getElementById(
    "error-relativo"
  ).className = `stat-value ${errorClass}`;

  // Badge de evaluación
  document.getElementById("evaluacion-badge").textContent =
    data.validacion.evaluacion.charAt(0).toUpperCase() + data.validacion.evaluacion.slice(1);
  document.getElementById("evaluacion-badge").className = `evaluacion-badge ${errorClass}`;

  // Coordenadas Geográficas
  document.getElementById("lat-min").textContent = `${data.coordenadas_geograficas.min_lat.toFixed(4)}°`;
  document.getElementById("lat-max").textContent = `${data.coordenadas_geograficas.max_lat.toFixed(4)}°`;
  document.getElementById("lon-min").textContent = `${data.coordenadas_geograficas.min_lon.toFixed(4)}°`;
  document.getElementById("lon-max").textContent = `${data.coordenadas_geograficas.max_lon.toFixed(4)}°`;

  // Coordenadas Proyectadas
  document.getElementById("x-min").textContent = `${data.coordenadas_proyectadas.min_x.toLocaleString()} m`;
  document.getElementById("x-max").textContent = `${data.coordenadas_proyectadas.max_x.toLocaleString()} m`;
  document.getElementById("y-min").textContent = `${data.coordenadas_proyectadas.min_y.toLocaleString()} m`;
  document.getElementById("y-max").textContent = `${data.coordenadas_proyectadas.max_y.toLocaleString()} m`;
  document.getElementById("proyeccion-info").textContent = `Proyección: ${data.proyeccion}`;

  // Bounding Box
  document.getElementById("bbox-ancho").textContent = `${data.bounding_box.ancho_km.toLocaleString()} km`;
  document.getElementById("bbox-alto").textContent = `${data.bounding_box.alto_km.toLocaleString()} km`;
  document.getElementById("bbox-area").textContent = `${data.bounding_box.area_km2.toLocaleString()} km²`;

  // Estadísticas de simulación
  document.getElementById("total-puntos").textContent =
    data.simulacion.n_puntos.toLocaleString();
  document.getElementById("puntos-dentro").textContent =
    data.simulacion.puntos_dentro.toLocaleString();
  document.getElementById("puntos-fuera").textContent =
    data.simulacion.puntos_fuera.toLocaleString();
  document.getElementById(
    "tiempo-sim"
  ).textContent = `${data.simulacion.tiempo_segundos} seg`;

  // Cálculo del área
  document.getElementById("area-bbox").textContent =
    `${data.simulacion.area_bbox_km2.toLocaleString()} km²`;
  document.getElementById("proporcion").textContent =
    data.simulacion.proporcion.toFixed(6);
  document.getElementById("area-estimada-calc").innerHTML =
    `<strong>${data.simulacion.area_estimada_km2.toLocaleString()} km²</strong>`;

  // Validación
  document.getElementById("area-real-val").textContent =
    `${data.validacion.area_real_km2.toLocaleString()} km²`;
  document.getElementById("area-calc-val").textContent =
    `${data.validacion.area_estimada_km2.toLocaleString()} km²`;
  document.getElementById("error-absoluto").textContent =
    `${data.validacion.error_absoluto_km2.toLocaleString()} km²`;
  document.getElementById("error-relativo-val").textContent =
    `${data.validacion.error_relativo_porcentaje}%`;

  // Mensaje de precisión
  document.getElementById("mensaje-precision").textContent = data.validacion.mensaje_precision;
  document.getElementById("mensaje-precision").className = `mensaje-precision ${errorClass}`;

  // Mostrar visualizaciones
  document.getElementById(
    "visualizacion-previa"
  ).src = `data:image/png;base64,${data.visualizacion_previa}`;
  document.getElementById(
    "visualizacion-simulacion"
  ).src = `data:image/png;base64,${data.visualizacion_simulacion}`;

  // Mostrar sección de resultados
  document.getElementById("resultados").classList.remove("hidden");

  // Scroll suave a resultados
  document
    .getElementById("resultados")
    .scrollIntoView({ behavior: "smooth", block: "start" });
}

