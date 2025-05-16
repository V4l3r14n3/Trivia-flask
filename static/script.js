let preguntaActual = null;
let respondido = false;

async function cargarPregunta() {
  respondido = false;
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
    btn.disabled = false;
    btn.onclick = () => verificarRespuesta(opcion, btn);
    opcionesDiv.appendChild(btn);
  });

  document.getElementById("siguiente-btn").disabled = true;
}

async function verificarRespuesta(opcionElegida, btn) {
  if (respondido) return; // evitar múltiples respuestas
  respondido = true;

  const res = await fetch(`/respuesta/${preguntaActual.id}`);
  const data = await res.json();
  const correcta = data.respuesta;

  const opcionesDiv = document.getElementById("opciones");
  // Deshabilitar todos los botones
  Array.from(opcionesDiv.children).forEach(button => button.disabled = true);

  if (opcionElegida === correcta) {
    btn.style.backgroundColor = "#4CAF50"; // verde
    document.getElementById("respuesta").innerText = "✅ ¡Correcto!";
  } else {
    btn.style.backgroundColor = "#F44336"; // rojo
    // Resaltar la opción correcta también
    Array.from(opcionesDiv.children).forEach(button => {
      if (button.innerText === correcta) {
        button.style.backgroundColor = "#4CAF50";
      }
    });
    document.getElementById("respuesta").innerText = `❌ Incorrecto. La respuesta correcta es: ${correcta}`;
  }

  document.getElementById("siguiente-btn").disabled = false;
}

window.onload = cargarPregunta;
