import openai
import json


# Clase para utilizar cualquier LLM para procesar un texto
# Y regresar una funcion a llamar con sus parametros
# Uso el modelo 0613, pero puedes usar un poco de
# prompt engineering si quieres usar otro modelo
class LLM:
    def __init__(self):
        pass

    def process_functions(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                # Si no te gusta que te hable feo, cambia aqui su descripcion
                {"role": "system", "content": "Eres un asistente amable"},
                {"role": "user", "content": text},
            ],
            functions=[
                {
                    "name": "get_weather",
                    "description": "Obtener el clima actual",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ubicacion": {
                                "type": "string",
                                "description": "La ubicación, debe ser una ciudad",
                            }
                        },
                        "required": ["ubicacion"],
                    },
                },
                {
                    "name": "actividad_semana",
                    "description": "establecer una actividad semanal, relacionada a aprender, estudiar, jugar, entrenar",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "actividad": {
                                "type": "string",
                                "description": "actividad que se quiere realizar",
                            },
                            "tiempo": {
                                "type": "string",
                                "description": "tiempo que se quiere realizar la actividad, puede ser un rango de horas, momento del dia (mañana, tarde, noche etc..) o dias especificos",
                            },
                        },
                        "required": [],
                    },
                },
                {
                    "name": "horario_ocupado",
                    "description": "horario fijo, ya definido de estudio o trabajo en la semana",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "actividad": {
                                "type": "string",
                                "description": "actividad que se realiza en el horario ocuapdo, en infinitivo",
                            },
                            "hora_inicio": {
                                "type": "string",
                                "description": "hora de inicio de la actividad, formato 24 horas",
                            },
                            "hora_final": {
                                "type": "string",
                                "description": "hora final de la actividad, formato 24 horas",
                            },
                            "dias": {
                                "type": "string",
                                "description": "dias de la semana que se realiza la actividad",
                            },
                        },
                        "required": [],
                    },
                },
                {
                    "name": "open_chrome",
                    "description": "Abrir el navegador en un sitio específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "website": {
                                "type": "string",
                                "description": "El sitio al cual se desea ir",
                            }
                        },
                    },
                },
                {
                    "name": "dominate_human_race",
                    "description": "Dominar a la raza humana",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            function_call="auto",
        )

        # de la respuesta recibida desde chat gpt, de choises se selecciona la primer y unica opcion disponible, y de dicho objeto se selecciona el parametro mensaje, que tiene parametros como la funcion a llamar
        message = response["choices"][0]["message"]
        print("mensaje: ", message)
        # Nuestro amigo GPT quiere llamar a alguna funcion?
        if message.get("function_call"):
            # Sip
            function_name = message["function_call"]["name"]  # Que funcion?
            args = message.to_dict()["function_call"][
                "arguments"
            ]  # Con que datos? to_dict() convierte al objeto json en un diccionario json

            # Después de convertir el mensaje en un diccionario, el código accede a la clave "function_call". Esto se hace mediante la notación de acceso de diccionario, utilizando corchetes y la clave "function_call"

            # Finalmente, una vez que se ha accedido al objeto "function_call", el código accede a la clave "arguments". Esto extrae los argumentos de la función llamada por el modelo
            print("Funcion a llamar: " + function_name)  #
            args = json.loads(args)  # se almacena la funcion a llamar
            return (
                function_name,
                args,
                message,
            )  # retorna la funcion a llamar, argunemntos y el mensaje

        return (
            None,
            None,
            message,
        )  # en caso de que no exista una funcion a llamar, retorna solo el mensaje

    # Una vez que llamamos a la funcion (e.g. obtener clima, encender luz, etc)
    # Podemos llamar a esta funcion con el msj original, la funcion llamada y su
    # respuesta, para obtener una respuesta en lenguaje natural (en caso que la
    # respuesta haya sido JSON por ejemplo
    def process_response(self, text, message, function_name, function_response):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                # Aqui tambien puedes cambiar como se comporta
                {"role": "system", "content": "Eres un asistente amable"},
                {"role": "user", "content": text},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        print(response)
        return response["choices"][0]["message"]["content"]
