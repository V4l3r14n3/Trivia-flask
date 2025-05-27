let preguntaActual = null;
let respondido = false;
let vidas = 3;

async function cargarPregunta() {
  respondido = false;
  const res = await fetch("/pregunta/aleatoria");
  const data = await res.json();

  if (data.error) {
    Swal.fire({
      title: 'Error',
      text: data.error,
      icon: 'error',
      confirmButtonText: 'Volver al inicio',
      background: '#2c5364',
      color: '#fff',
      confirmButtonColor: '#ee8d1f'
    }).then(() => {
      window.location.href = "/";
    });
    return;
  }

  preguntaActual = data;
  vidas = data.vidas;
  actualizarVidas();

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

function actualizarVidas() {
  document.getElementById("vidas").innerText = `❤️ Vidas: ${vidas}`;
}

async function verificarRespuesta(opcionElegida, btn) {
  if (respondido) return;
  respondido = true;

  const res = await fetch(`/respuesta/${preguntaActual.id}`);
  const data = await res.json();
  const correcta = data.respuesta;

  const opcionesDiv = document.getElementById("opciones");
  Array.from(opcionesDiv.children).forEach(button => button.disabled = true);

  if (opcionElegida === correcta) {
    btn.style.backgroundColor = "#4CAF50";
    document.getElementById("respuesta").innerText = "✅ ¡Correcto!";
  } else {
    vidas--;
    await fetch("/vidas/perder");
    actualizarVidas();
    btn.style.backgroundColor = "#F44336";

    // Mostrar cuál era la correcta
    Array.from(opcionesDiv.children).forEach(button => {
      if (button.innerText === correcta) {
        button.style.backgroundColor = "#4CAF50";
      }
    });

    document.getElementById("respuesta").innerText = `❌ Incorrecto. La respuesta correcta es: ${correcta}`;

    // Si ya no quedan vidas, esperar 5 segundos antes de mostrar la alerta
    if (vidas <= 0) {
      setTimeout(() => {
        Swal.fire({
          title: '¡Juego Terminado!',
          text: 'Perdiste todas tus vidas 😢',
          icon: 'error',
          confirmButtonText: 'Volver al inicio',
          background: '#2c5364',
          color: '#fff',
          confirmButtonColor: '#ee8d1f'
        }).then(() => {
          window.location.href = "/";
        });
      }, 3000);
      return;
    }
  }

  document.getElementById("siguiente-btn").disabled = false;
}

window.onload = cargarPregunta;
