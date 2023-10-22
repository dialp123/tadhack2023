import openai

#Convertir audio en texto
class Transcriber:
    # es el constructor de la clase. El parámetro self es una referencia al objeto que se está creando. En Python, se debe incluir self como primer parámetro en todos los métodos de clase para que puedan acceder a los atributos y métodos del objeto
    def __init__(self):
        #pass como un no-op, es decir, no realiza ninguna operación.
        pass
    #el constructor __init__ de la clase Transcriber no realiza ninguna operación específica al crear una instancia de la clase. Su función principal es servir como un punto de inicialización para los objetos de la clase, 

    #Siempre guarda y lee del archivo audio.mp3
    #Utiliza whisper en la nube :) puedes cambiarlo por una impl local
    def transcribe(self, audio):
        audio.save("audio.mp3")
        audio_file= open("audio.mp3", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript.text