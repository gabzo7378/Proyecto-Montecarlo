const API_URL = "http://localhost:8000";

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
      option.textContent = `${
        pais.nombre
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
  // Actualizar valores
  document.getElementById("pais-nombre").textContent = data.pais;
  document.getElementById(
    "area-real"
  ).textContent = `${data.area_real_km2.toLocaleString()} km²`;
  document.getElementById(
    "area-estimada"
  ).textContent = `${data.simulacion.area_estimada_km2.toLocaleString()} km²`;

  const errorClass =
    data.validacion.error_relativo_porcentaje < 1
      ? "success"
      : data.validacion.error_relativo_porcentaje < 5
      ? "warning"
      : "error";
  document.getElementById(
    "error-relativo"
  ).textContent = `${data.validacion.error_relativo_porcentaje}%`;
  document.getElementById(
    "error-relativo"
  ).className = `stat-value ${errorClass}`;

  document.getElementById("total-puntos").textContent =
    data.simulacion.n_puntos.toLocaleString();
  document.getElementById("puntos-dentro").textContent =
    data.simulacion.puntos_dentro.toLocaleString();
  document.getElementById("puntos-fuera").textContent =
    data.simulacion.puntos_fuera.toLocaleString();
  document.getElementById(
    "tiempo-sim"
  ).textContent = `${data.simulacion.tiempo_segundos} seg`;
  document.getElementById("proporcion").textContent =
    data.simulacion.proporcion.toFixed(6);

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
