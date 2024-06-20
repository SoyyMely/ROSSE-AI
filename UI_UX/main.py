import customtkinter
from PIL import Image, ImageTk
import sys
import threading
import google.generativeai as genai
import key
import tkinter as tk
from tkinter import Text, END
import os
import sys
# Configuración de la apariencia y el tema
customtkinter.set_appearance_mode("Dark")  # Modos: "System" (estándar), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Temas: "blue" (estándar), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self, user_email):
        super().__init__()

        self.title("ROSSE AI")
        self.geometry(f"{1100}x{580}")
        self.iconbitmap("./imagenes/a.ico")
        self.configure_grid()
        self.create_sidebar(user_email)
        self.create_main_area()
            # Configurar etiquetas para estilos de texto
        self.textbox.tag_configure('user', foreground='white', font=('Arial', 11, 'bold'), wrap='word', justify='right', lmargin1=50, rmargin=50, spacing3=5)
        self.textbox.tag_configure('ai', foreground='white', font=('Arial', 12, 'bold'), wrap='word', justify='left', lmargin1=50, rmargin=50, spacing3=5)
        self.user_icon = Image.open("./imagenes/user.png")
        self.user_icon = self.user_icon.resize((20, 20), Image.Resampling.LANCZOS)
        self.user_photo = ImageTk.PhotoImage(self.user_icon)
            # Carga y redimensiona el icono de ROSSE AI
        self.ai_icon = Image.open("./imagenes/a.png")  # Asegúrate de que la ruta y el nombre del archivo sean correctos
        self.ai_icon = self.ai_icon.resize((45,30), Image.Resampling.LANCZOS)
        self.ai_photo = ImageTk.PhotoImage(self.ai_icon)

        self.create_footer()
        self.load_api_key()
        self.display_temporary_image_text()
        


    def configure_grid(self):
        # Configura el diseño de la cuadrícula (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def create_sidebar(self, user_email):
        # Crea la barra lateral con widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0, fg_color="#212121")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

            # Icono de nuevo chat alineado a la izquierda
        self.create_icon("./imagenes/a.png", "             Nuevo Chat", self.sidebar_frame, 30, 20, 0, 0, 'w')

        # Icono de usuario alineado a la derecha
        self.create_icon("./imagenes/newchat.png", "", self.sidebar_frame, 15, 15, 0, 1, 'e', command=self.reset_textbox)

        # Icono del usuario sin texto adicional, posiblemente en otra fila o con manejo especial para alinear a la derecha
        self.create_icon("./imagenes/user.png", "    " + user_email, self.sidebar_frame, 20, 20, 5, )

        
    def display_temporary_image_text(self):
        # Load and configure the image
        image_path = "./imagenes/a.png"
        image = Image.open(image_path)
        image = image.resize((350, 300))  # Resize the image to fit the label
        photo = ImageTk.PhotoImage(image)

        # Create and configure the label to display the image and text
        text = "Hola, ¿Cómo puedo ayudarte hoy?"
        self.label = customtkinter.CTkLabel(self, text=text, image=photo, compound="top")
        self.label.grid(row=0, column=1, columnspan=4, padx=(40, 40), pady=(40, 10), sticky="nsew")
        self.label.image = photo  # Keep a reference to avoid garbage collection

        # Configure the font and style of the text
        self.label.configure(font=("Arial", 24, "bold"))  # Use 'bold' as part of the font configuration

        # Schedule the deletion of the label after 3 seconds
        self.after(7000, self.delete_label)

    def delete_label(self):
        # Delete the label
        if hasattr(self, 'label'):
            self.label.destroy()


    def create_icon(self, path, text, frame, width, height, row, column=0, sticky='w', command=None):
        image = Image.open(path)
        image = image.resize((width, height))
        photo = ImageTk.PhotoImage(image)
        label = customtkinter.CTkLabel(frame, image=photo, text=text, compound='left')
        label.image = photo  # keep a reference
        label.grid(row=row, column=column, padx=20, pady=(10, 10), sticky=sticky)
        if command:
            label.bind("<Button-1>", command)  # Vincular el evento de clic al handler proporcionado




    def create_main_area(self):
        # Crea la zona principal
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Habla con ROSSE")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.textbox = Text(self, state='disabled', bg='#212121', fg='white', font=("Helvetica", 12), wrap='word', bd=0, highlightthickness=0, relief='flat')
        self.textbox.grid(row=0, column=1, columnspan=4, padx=(40, 40), pady=(40, 10), sticky="nsew")
       

    def create_footer(self):
        # Crea el footer con botones de enviar y micrófono
        self.create_send_button()
        self.create_microphone_button()

    def create_send_button(self):
        self.send_button = self.create_button("./imagenes/enviar.png", "", self.send_to_api, 20, 20)
        self.send_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    

    #AQUI ES DONDE ESTA LA CONEXION DEL BOTON
    def create_microphone_button(self):
     self.microphone_button = self.create_button("./imagenes/microphone.png", "", self.run_test_py, 20, 20)
     self.microphone_button.grid(row=3, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def run_test_py(self):
        import subprocess
        
        # Construir la ruta absoluta al archivo
        script_path = os.path.join(os.path.dirname(__file__), 'prueba.py')
        
        # Verificar si el archivo existe antes de intentar ejecutarlo
        if os.path.exists(script_path):
            # Llamar al script de Python de manera segura
            subprocess.run([sys.executable, script_path])
            sys.exit()
        else:
            print(f"Error: No se encontró el archivo {script_path}")
        #AQUI TERMINA LA CONEXION DEL BOTON

    def create_button(self, path, text, command, width, height):
        image = Image.open(path)
        image = image.resize((width, height))
        photo = ImageTk.PhotoImage(image)
        button = customtkinter.CTkButton(self, image=photo, text=text, command=command, fg_color="#00c4cc", corner_radius=20, height=40, width=6, hover_color=("gray75", "gray20"))
        button.image = photo  # keep a reference!
        return button
    
    def reset_textbox(self, event=None):  # Añade event como parámetro, con un valor predeterminado de None
        # Eliminar el textbox actual
        self.textbox.destroy()
        
        # Crear un nuevo textbox
        self.textbox = Text(self, state='disabled', bg='#212121', fg='white', font=("Helvetica", 12), wrap='word', bd=0, highlightthickness=0, relief='flat')
        self.textbox.grid(row=0, column=1, columnspan=4, padx=(40, 40), pady=(40, 10), sticky="nsew")

        

    def send_to_api(self):
        input_text = self.entry.get().strip()
        if input_text:
            self.textbox.configure(state='normal')
            # Inserta el texto del usuario al final del widget de texto
            self.textbox.insert(END, f"{input_text}  ",   'user')  # Añade un espacio para separación visual
            # Crea un índice donde insertar la imagen para que aparezca a la derecha del texto
            image_index = self.textbox.index('insert -0 chars')
            self.textbox.image_create(image_index, image=self.user_photo)
            self.textbox.insert(END, '\n')  # Añade una nueva línea después de la imagen
            self.entry.delete(0, 'end')
            self.textbox.configure(state='disabled')
            self.send_button.configure(state='disabled')
            threading.Thread(target=self.get_response_from_api, args=(input_text,)).start()


    def get_response_from_api(self, input_text):
        try:
            genai.configure(api_key=key.clave)
            model = genai.GenerativeModel(model_name="gemini-pro")
            response = model.generate_content(input_text)
            self.textbox.configure(state='normal')
            if response.text:
                # Crea un índice para insertar el icono antes del texto
                self.textbox.insert(END, '\n')  # Asegúrate de que la respuesta comienza en una nueva línea
                image_index = self.textbox.index('end -1 chars')
                self.textbox.image_create(image_index, image=self.ai_photo)
                # Inserta el texto de la IA después del icono
                self.textbox.insert(END, f" {response.text}\n", 'ai')
            self.textbox.configure(state='disabled')
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.entry.configure(state='normal')
            self.send_button.configure(state='normal')
            self.textbox.see('end')




# Recuerda remover los print statements antes de lanzar la aplicación.




    def load_api_key(self):
        # Carga la API key desde una variable de entorno
        # Esta función debe implementarse con tu lógica de carga de clave API
        pass
    
    
if __name__ == "__main__":
    email_arg = sys.argv[1] if len(sys.argv) > 1 else "username@fulanito"
    app = App(email_arg)
    app.mainloop()