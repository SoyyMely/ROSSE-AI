from customtkinter import *
import pyttsx3
import speech_recognition as sr
import threading
import ctypes
from tkinter import PhotoImage

# Inicializa el reconocedor de voz y el motor de TTS (text-to-speech)
r = sr.Recognizer()
engine = pyttsx3.init()

def clean_text(text):
    text = text.replace('*', '')  # Elimina asteriscos
    text = text.replace('#', '')  # Elimina almohadillas
    return text

def speak(text, canvas=None, light=True):
    cleaned_text = clean_text(text)
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'spanish' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(cleaned_text)
    engine.runAndWait()

def get_response_from_api(input_text, app, canvas):
    app.update_response(f"Tú: {input_text}")  # Visualizar el mensaje de envío
    # Aquí puedes incluir el código para obtener una respuesta de la API, como lo hacías antes
    pass

def send_to_api(solicitud, app, canvas):
    threading.Thread(target=get_response_from_api, args=(solicitud, app, canvas)).start()

def listen_and_respond(app, canvas):
    speak("Hola, soy Rrous, ¿en qué puedo ayudarte hoy?", canvas)
    app.update_response("Hola, soy Rosse, ¿en qué puedo ayudarte hoy?")
    while True:
        with sr.Microphone() as source:
            try:
                audio = r.listen(source)
                text = r.recognize_google(audio, language='es-ES')
                send_to_api(text, app, canvas)
                app.update_response(f"user: {text}")
            except sr.UnknownValueError:
                speak("No pude entender el audio, intenta de nuevo.", canvas)
            except sr.RequestError as e:
                speak(f"Error de servicio: {e}", canvas)
        speak("", canvas, light=False)  # Apaga cualquier luz

def pause_action():
    # Esta función se ejecutará cuando se haga clic en el botón de pausa
    pass

def play_action():
    # Esta función se ejecutará cuando se haga clic en el botón de reproducir
    pass

class AnimatedBoxes:
    def __init__(self, root, screen_width, screen_height):
        self.root = root
        self.canvas = CTkCanvas(root, width=300, height=200, bg=azulFondo, highlightbackground=azulFondo)
        self.canvas.place(x=(screen_width - 300) / 2, y=(screen_height - 200) / 2)

        # Crear cuadros
        self.boxes = [
            self.canvas.create_rectangle(50, 75, 100, 125, fill="#606060"),
            self.canvas.create_rectangle(110, 75, 160, 125, fill="#606060"),
            self.canvas.create_rectangle(170, 75, 220, 125, fill="#606060"),
            self.canvas.create_rectangle(230, 75, 280, 125, fill="#606060")
        ]
        
        self.current_box = 0
        self.move_up = True
        self.animate()

        # Crear el área de respuesta
        self.response_area = CTkTextbox(root, height=20, width=80)
        self.response_area.place(x=10, y=400)  #
        self.response_area = CTkTextbox(root, height=20, width=80)
        

    def animate(self):
        # Ciclo que mueve un cuadro a la vez
        move_distance = -2 if self.move_up else 1  # Reducir el movimiento para una animación más suave
        self.canvas.move(self.boxes[self.current_box], 0, move_distance)

        # Actualizar cuadro actual y dirección
        self.current_box = (self.current_box + 1) % 4
        if self.current_box == 0:
            self.move_up = not self.move_up

        # Llama a sí mismo después de un tiempo más corto para una animación más fluida
        self.root.after(50, self.animate)
    
    def update_response(self, text):
        self.response_area.insert('end', text + "\n")
        self.response_area.yview('end')

# Obtener el tamaño de la pantalla
user32 = ctypes.windll.user32
screen_width = 1100
screen_height = 580
azulFondo = "#1A1A1A"

# Crear y configurar la ventana
root = CTk()
root.title("ROSSE AI")
root.iconbitmap("./imagenes/a.ico")
set_appearance_mode("dark")
root.geometry(f"{screen_width}x{screen_height}")
root.config(background=azulFondo)

# Crear la instancia de AnimatedBoxes
app = AnimatedBoxes(root, screen_width, screen_height)



# Iniciar el hilo para escuchar y responder al usuario
threading.Thread(target=listen_and_respond, args=(app, None), daemon=True).start()

root.mainloop()
