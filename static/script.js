let preguntaActual = null;

async function cargarPregunta() {
  const res = await fetch("/pregunta/aleatoria");
  const data = await res.json();
  preguntaActual = data;

  document.getElementById("pregunta").innerText = data.pregunta;
  document.getElementById("respuesta").innerText = "";
  const opcionesDiv = document.getElementById("opciones");
  opcionesDiv.innerHTML = "";

  data.opciones.forEach(opcion => {
    const btn = document.createElement("button");
    btn.className = "opcion-btn";
    btn.innerText = opcion;
    btn.onclick = () => verificarRespuesta(opcion);
    opcionesDiv.appendChild(btn);
  });
}

async function verificarRespuesta(opcionElegida) {
  const res = await fetch(`/respuesta/${preguntaActual.id}`);
  const data = await res.json();
  const correcta = data.respuesta;

  const mensaje = opcionElegida === correcta ? "✅ ¡Correcto!" : `❌ Incorrecto. La respuesta correcta es: ${correcta}`;
  document.getElementById("respuesta").innerText = mensaje;
}

window.onload = cargarPregunta;
