from subprocess import call
import webbrowser

#Clase para ejecutar comandos en la PC
#De momento esta en duro funcional para Windows hohoh
class PcCommand():
    def __init__(self):
        pass
    
    def open_chrome(self, website):
        website = "" if website is None else website
        #Funciona para windows, si quieres para otro, modificalo!! :D
        # call("/usr/lib/firefox-esr/firefox-esr " + website)
        webbrowser.open(website)