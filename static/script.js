let preguntaActual = null;

async function cargarPregunta() {
  const res = await fetch("/pregunta/aleatoria");
  const data = await res.json();
  preguntaActual = data;
  document.getElementById("pregunta").innerText = data.pregunta;
  document.getElementById("respuesta").innerText = "";
}

async function verRespuesta() {
  if (preguntaActual) {
    const res = await fetch(`/respuesta/${preguntaActual.id}`);
    const data = await res.json();
    document.getElementById("respuesta").innerText = "Respuesta: " + data.respuesta;
  }
}

window.onload = cargarPregunta;