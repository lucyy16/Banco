import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import pyttsx3
import os

# --- CONFIGURACIÓN DE VOZ ---
engine = pyttsx3.init()
def hablar(texto):
    print(f"Asistente: {texto}")
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    r = sr.Recognizer()
    fs = 44100
    segundos = 4 
    try:
        print("\n[Escuchando...]")
        grabacion = sd.rec(int(segundos * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        write('temp_audio.wav', fs, grabacion)
        with sr.AudioFile('temp_audio.wav') as source:
            audio = r.record(source)
            comando = r.recognize_google(audio, language='es-MX')
            return comando.lower()
    except:
        return ""

# --- FUNCIONES BANCARIAS ---
def guardar_movimiento(detalle):
    with open("movimientos.txt", "a") as f:
        f.write(detalle + "\n")

# --- VARIABLES INICIALES ---
NOMBRE_ASISTENTE = "banquero"
PIN_CORRECTO = "1 2 3 4"
saldo = 5000 # Saldo inicial ficticio

hablar(f"Sistema activado. Di {NOMBRE_ASISTENTE} para iniciar.")

while True:
    voz = escuchar()
    
    if NOMBRE_ASISTENTE in voz:
        hablar("¿Qué deseas hacer hoy?")
        accion = escuchar()
        
        if "transferencia" in accion:
            hablar("¿A quién enviaremos dinero?")
            contacto = escuchar()
            hablar("¿Qué cantidad?")
            monto = escuchar() # Intentará captar el número
            
            hablar(f"Confirmando {monto} pesos para {contacto}. Dicta tu PIN.")
            pin_ingresado = escuchar()
            
            if PIN_CORRECTO in pin_ingresado:
                # Actualizar saldo y guardar
                try:
                    valor = int(''.join(filter(str.isdigit, monto))) # Extrae solo números
                    saldo -= valor
                    guardar_movimiento(f"Transferencia de {valor} a {contacto}")
                    hablar(f"Éxito. Tu nuevo saldo es de {saldo} pesos.")
                except:
                    hablar("Transferencia realizada, pero no pude procesar el monto exacto.")
            else:
                hablar("PIN incorrecto.")

        elif "movimientos" in accion or "historial" in accion:
            hablar("Consultando tus últimos movimientos.")
            if os.path.exists("movimientos.txt"):
                with open("movimientos.txt", "r") as f:
                    lineas = f.readlines()
                    ultimo = lineas[-1] if lineas else "No hay movimientos"
                    hablar(f"Tu última operación fue: {ultimo}")
            else:
                hablar("Aún no tienes movimientos registrados.")

        elif "salir" in accion:
            hablar("Sesión cerrada.")
            break