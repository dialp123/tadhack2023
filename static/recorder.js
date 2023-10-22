import {
  getDatabase,
  ref,
  onValue,
} from "https://www.gstatic.com/firebasejs/10.5.0/firebase-database.js";

// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.5.0/firebase-app.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBKhzTYHa_i1AZVK0svPPNXYNEITKrd5Kc",
  authDomain: "tadhack2023.firebaseapp.com",
  projectId: "tadhack2023",
  storageBucket: "tadhack2023.appspot.com",
  messagingSenderId: "920289201504",
  appId: "1:920289201504:web:c424cf63a82d23a168a205",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase();

function parseTimeToTimestamp(timeString) {
  const [hours, minutes, seconds] = timeString.split(":");
  const today = new Date();
  today.setHours(parseInt(hours, 10));
  today.setMinutes(parseInt(minutes, 10));
  today.setSeconds(parseInt(seconds, 10));
  return today.getTime();
}

let blobs = [];
let stream;
let rec;
let recordUrl;
let audioResponseHandler;

export function recorder(url, handler) {
  recordUrl = url;
  if (typeof handler !== "undefined") {
    audioResponseHandler = handler;
  }
}

//   listening cambios en real time database
const starCountRef = ref(db, "TheStudents/");
let isFirstExecution = true;
onValue(starCountRef, (snapshot) => {
  const data = snapshot.val();
  if (isFirstExecution) {
    isFirstExecution = false;
  } else {
    if (data) {
      let elementoMasReciente = null;
      let horaMasReciente = 0;

      for (const key in data) {
        const elemento = data[key];
        const hora = parseTimeToTimestamp(elemento.hora);

        if (hora > horaMasReciente) {
          horaMasReciente = hora;
          elementoMasReciente = elemento;
        }
      }

      if (elementoMasReciente) {
        console.warn(elementoMasReciente.texto);

        var fd = new FormData();
        fd.append("stt", elementoMasReciente.texto);
        fd.append("tiempoOcupado", localStorage.getItem("tiempoOcupado"));

        fetch(recordUrl, {
          method: "POST",
          body: fd,
        })
          .then((response) => response.json())
          .then(audioResponseHandler)
          .catch((err) => {
            console.log("Oops: Ocurrió un error", err);
          });
      } else {
        console.warn("No se encontraron datos válidos");
      }
    } else {
      console.warn("Valor predeterminado");
    }
  }
});

//Llamar al handler en caso que exista
function handleAudioResponse(response) {
  if (!response || response == null) {
    //TODO subscribe you thief
    console.log("No response");
    return;
  }

  document.getElementById("record").style.display = "";
  document.getElementById("stop").style.display = "none";

  if (audioResponseHandler != null) {
    audioResponseHandler(response);
  }
}
