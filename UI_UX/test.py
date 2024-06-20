import numpy as np
import pyaudio
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import key2
import threading
import customtkinter as ctk
from tkinter import Canvas
import subprocess

# Configuración de PyAudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()

# Inicializa el reconocedor de voz y el motor de TTS (text-to-speech)
r = sr.Recognizer()
engine = pyttsx3.init()

def clean_text(text):
    text = text.replace('*', '')  # Elimina asteriscos
    text = text.replace('#', '')  # Elimina almohadillas
    return text

def speak(text):
    cleaned_text = clean_text(text)
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'spanish' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(cleaned_text)
    engine.runAndWait()

def get_response_from_api(input_text, app):
    app.update_response(f"Tú: {input_text}")  # Visualizar el mensaje de envío
    try:
        genai.configure(api_key=key2.clave2)
        model = genai.GenerativeModel(model_name="gemini-pro")
        response = model.generate_content(input_text)
        if response.text:
            app.update_response(response.text)  # Visualizar la respuesta
            speak(response.text)
        else:
            speak("Rosse no pudo procesar una respuesta.")
    except Exception as e:
        speak(f"Se produjo un error al obtener la respuesta de la API: {e}")

def send_to_api(solicitud, app):
    threading.Thread(target=get_response_from_api, args=(solicitud, app)).start()

def listen_and_respond(app):
    speak("Hola, soy Rrous, ¿en qué puedo ayudarte hoy?")
    app.update_response("Hola, soy Rosse, ¿en qué puedo ayudarte hoy?")
    while True:
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language='es-ES')
                send_to_api(text, app)
            except sr.UnknownValueError:
                speak("No pude entender el audio, intenta de nuevo.")
            except sr.RequestError as e:
                speak(f"Error de servicio: {e}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Asistente de Voz Rosse")
        self.geometry("800x600")

        self.canvas = Canvas(self, width=350, height=100, bg='#242424', highlightbackground='#242424')
        self.canvas.pack(pady=80)

        self.response_area = ctk.CTkTextbox(self, height=280, width=800, state='normal')
        self.response_area.place(x=0, y=300)

        self.bars = []
        bar_count = 6
        bar_width = 30
        bar_spacing = 10
        bar_max_height = 100
        bar_x_start = (350 - (bar_width * bar_count + bar_spacing * (bar_count - 1))) / 2

        for i in range(bar_count):
            bar_x = bar_x_start + (bar_width + bar_spacing) * i
            bar = self.canvas.create_rectangle(bar_x, 50, bar_x + bar_width, 50, fill="white", outline="")
            self.bars.append(bar)

        self.stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        self.update_visualizer()
        threading.Thread(target=listen_and_respond, args=(self,), daemon=True).start()

        # Agregar el manejo de la tecla Esc para cerrar la aplicación
        self.bind("<Escape>", self.on_closing)

    def update_visualizer(self):
        try:
            data = np.frombuffer(self.stream.read(CHUNK), dtype=np.int16)
            fft_data = np.fft.rfft(data)
            magnitudes = np.abs(fft_data)[:len(self.bars)] * 2 / (32768 * CHUNK)

            for i, mag in enumerate(magnitudes):
                bar_x = (350 - (30 * 6 + 10 * (6 - 1))) / 2 + (30 + 10) * i
                bar_height = min(mag * 5000, 100)
                bar_y = 100 - bar_height
                self.canvas.coords(self.bars[i], bar_x, bar_y, bar_x + 30, 100)
        except Exception as e:
            print("Error en la visualización:", e)

        self.after(10, self.update_visualizer)

    def update_response(self, text):
        self.response_area.insert('end', text + "\n")
        self.response_area.yview('end')

    def on_closing(self, event=None):
        self.stream.stop_stream()
        self.stream.close()
        p.terminate()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
