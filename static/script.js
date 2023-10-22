let actividades = [];
try {
  actividades = JSON.parse(localStorage.getItem("actividades")) || [];
} catch (error) {
  actividades = [];
}

const semana = [
  "Lunes",
  "Martes",
  "Miércoles",
  "Jueves",
  "Viernes",
  "Sábado",
  "Domingo",
];

function generarTabla(eventos) {
  const coloresEventos = [
    "#4d4385",
    "#54a4b1",
    "#3047c9",
    "#473626",
    "#c74306",
    "#bc927b",
    // Agrega más colores si es necesario
  ];
  const coloresPorTitulo = {};

  if (!!eventos) {
    actividades = actividades.concat(eventos);
  }
  localStorage.setItem("actividades", JSON.stringify(actividades));

  let resultado = {};
  actividades.forEach((actividad) => {
    const { dia, horaInicio, horaFinal } = actividad;

    if (!resultado[dia]) {
      resultado[dia] = [];
    }

    resultado[dia].push({ horaInicio, horaFinal });
  });
  localStorage.removeItem("tiempoOcupado");
  localStorage.setItem("tiempoOcupado", JSON.stringify(resultado));

  actividades.forEach((evento) => {
    evento.titulo = capitalizarPrimeraLetra(evento.titulo);
    evento.dia = capitalizarPrimeraLetra(evento.dia);
  });

  const tablaBody = document.getElementById("tabla-rutina-body");

  while (tablaBody.firstChild) {
    tablaBody.removeChild(tablaBody.firstChild);
  }

  for (let hora = 7; hora <= 22; hora++) {
    const fila = document.createElement("tr");

    const horaCelda = document.createElement("td");
    horaCelda.textContent = hora + ":00";
    horaCelda.classList.add("container-cell");
    fila.appendChild(horaCelda);

    for (let dia of semana) {
      const celda = document.createElement("td");
      if (dia == "Domingo" || dia == "Sabado") {
      }

      celda.classList.add("container-cell");
      celda.classList.add("container-cell2");
      const celdaContent = document.createElement("div");
      celda.appendChild(celdaContent);

      const horaActual = hora + ":00";
      const eventosEnHora = actividades.filter(
        (e) =>
          e.dia === dia &&
          convertirHoraAMinutos(e.horaInicio) <=
            convertirHoraAMinutos(horaActual) &&
          convertirHoraAMinutos(e.horaFinal) > convertirHoraAMinutos(horaActual)
      );
      if (eventosEnHora.length > 0) {
        const evento = eventosEnHora[0];
        const duracionEvento = calcularDuracionEnHoras(evento);

        celda.rowSpan = duracionEvento;

        if (
          parseInt(evento.horaInicio.split(":")) ===
          parseInt(horaActual.split(":"))
        ) {
          celdaContent.textContent = evento.titulo;
          fila.appendChild(celda);
        }

        if (!coloresPorTitulo[evento.titulo]) {
          const colorIndex =
            Object.keys(coloresPorTitulo).length % coloresEventos.length;
          coloresPorTitulo[evento.titulo] = coloresEventos[colorIndex];
        }

        celdaContent.style.backgroundColor = coloresPorTitulo[evento.titulo];
        celdaContent.classList.add("content-cell");

        celda.addEventListener("click", function () {
          const htmlString = `<h2 style="rutina__titulo">${evento.titulo}</h2>
          <p>
          <b>📆 Dia:</b> ${evento.dia}<br>
          <b>⏰ Hora inicio:</b> ${evento.horaInicio}<br>
          <b>⏰ Hora final:</b> ${evento.horaFinal}<br> <br>
          ${
            evento.texto !== undefined
              ? `<b>🗒️ Recomendación:</b> ${evento.texto}<br>`
              : ""
          }
          </p>
          `;
          rutinaContainer.innerHTML = htmlString;
          rutinaContainer.style.backgroundColor =
            coloresPorTitulo[evento.titulo];
          rutinaContainer.style.display = "block";
        });
      } else {
        fila.appendChild(celda);
      }
    }
    tablaBody.appendChild(fila);
  }
}

function convertirHoraAMinutos(hora) {
  const [horas, minutos] = hora.split(":");
  return parseInt(horas) * 60 + parseInt(minutos);
}

function capitalizarPrimeraLetra(texto) {
  if (typeof texto === "string" && texto.length > 0) {
    return texto.charAt(0).toUpperCase() + texto.slice(1);
  } else {
    return "";
  }
}

function calcularDuracionEnHoras(evento) {
  const horaInicio = parseInt(evento.horaInicio.split(":")[0]);
  const horaFinal = parseInt(evento.horaFinal.split(":")[0]);
  return horaFinal - horaInicio;
}

function mostrarEventos(eventos) {
  const eventosDiv = document.querySelector("#eventos");
  eventosDiv.innerHTML = "<h2>Eventos</h2>";
  eventosDiv.innerHTML += "<ul>";
  eventos.forEach((evento) => {
    eventosDiv.innerHTML += `<li>${evento.titulo} - ${evento.dia} (${evento.horaInicio} - ${evento.horaFinal})</li>`;
  });
  eventosDiv.innerHTML += "</ul>";
}

// Llamar a las funciones
generarTabla(null);
localStorage.clear();
