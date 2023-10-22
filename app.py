import os
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request
import json
from transcriber import Transcriber
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand

# contraseña radisys Hs3@s3-g

# Cargar llaves del archivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("recorder.html")


@app.route("/audio", methods=["POST"])
def audio():
    # Obtener audio grabado y transcribirlo
    # audio = request.files.get("audio")
    tiempo_ocupado = request.form.get("tiempoOcupado")
    text = request.form.get("stt")

    print("texto stt", text)

    llm = LLM()
    function_name, args, message = llm.process_functions(text)
    if function_name is not None:
        # Si se desea llamar una funcion de las que tenemos

        if function_name == "horario_ocupado":
            # Llamar a la funcion para enviar un correo
            text = (
                "Responde solo con un array(sin nombre) de objetos JSON, sin texto adicional. Proporciona una rutina para los dias "
                + args["dias"]
                + " para la actividad "
                + args["actividad"]
                + ". Quiero que la actividad empiece todos los dias a la "
                + args["hora_inicio"]
                + " y termine a las"
                + args["hora_final"]
                + ". Quiero que la rutina tenga un campo titulo (por ejemplo, "
                + args["actividad"]
                + " con un emoji relacionado al inicio), un campo dia (por ejemplo, 'Lunes'), campo horaInicio y campo horaFinal de la actividad (formato 24 hrs)."
            )

            final_response = llm.process_response(text, message, function_name, "")

            audioText = (
                "Listo, ya programe tu rutina para "
                + args["actividad"]
                + "en los dias"
                + args["dias"]
                + " ¿Que actividades quieres realizar en tu tiempo libre?"
            )
            tts_file = TTS().process(audioText)
            return {
                "result": "ok",
                "text": final_response,
                "file": tts_file,
            }
        elif function_name == "actividad_semana":
            # Llamar a la funcion para enviar un correo
            text = (
                "Responde solo con un array(sin nombre) de objetos JSON, sin texto adicional. Proporciona una rutina semanal para "
                + args["actividad"]
                + ". Sabiendo que la horas para actividades va de 7:00 a 12:00 y de 14:00 a las 22:00, quiero que la actividad empiece y termine en horarios diferentes a los ya definidos en este json: "
                + tiempo_ocupado
                + " y tenga en cuenta estos posibles horarios (si es posible): "
                + (args["tiempo"] if args["tiempo"] else "Ninguno")
                + ", quiero que dure el tiempo recomendado para dicha actividad. Por ultimo quiero que la rutina tenga un campo titulo (por ejemplo, "
                + args["actividad"]
                + " con un emoji relacionado al inicio), un campo día (por ejemplo, 'Lunes'), un campo texto (con un maximo de 10 caracteres de recomendaciones o consejos relacionados con la actividad), campo horaInicio y campo horaFinal de la actividad (formato 24 hrs y que empiece en minutos HH:00)."
            )

            final_response = llm.process_response(text, message, function_name, "")

            audioText = (
                "Listo, ya programe tu rutina semanal para "
                + args["actividad"]
                + "en tu tiempo libre"
            )
            tts_file = TTS().process(audioText)
            return {
                "result": "ok",
                "text": final_response,
                "file": tts_file,
            }
    else:
        final_response = "No tengo idea de lo que estás hablando, Ringa Tech"
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}
