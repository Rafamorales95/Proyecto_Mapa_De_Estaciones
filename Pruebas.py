import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    user="root",
    host="localhost",
    database="proyecto_estaciones",
    port=3306
)

# Lista de estaciones de carga para seleccionar aleatoriamente con coordenadas de latitud y longitud
lista_estaciones = [

# Coordenadas de ejemplo en Bolívar, Santander


    ("Estación Crr24f#40f123",  6.229, -73.393),
    ("Estación C 7 45 #24 100", 6.232, -73.391),
    ("Estación  Cr 345 # 09 4", 6.231, -73.389)
]

# Clase Usuario
class Usuario:
    def __init__(self, nombre, contra):
        self.nombre = nombre
        self.contra = contra
        self.conectado = False

    def desconectar(self):
        if self.conectado:
            print("¡Se cerró sesión con éxito!")
            self.conectado = False
        else:
            print("Error, no inició sesión.")

    def __str__(self):
        conect = "conectado" if self.conectado else "desconectado"
        return f"Mi nombre de usuario es {self.nombre} y estoy {conect}"

# Función para conectar usuario
def conectar():
    nombre = nombreEntry.get()
    contra = passEntry.get()

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND contra = %s", (nombre, contra))
    usuario_data = cursor.fetchone()
    cursor.close()

    if usuario_data:
        messagebox.showinfo("Login Exitoso", "¡Usuario encontrado y contraseña correcta!")
        mostrar_estaciones_aleatorias()
    else:
        messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")

# Función para convertir coordenadas geográficas a coordenadas de píxeles en el mapa
def lat_lon_to_pixel(lat, lon, img_width, img_height):
    # Ajustar estos valores según las coordenadas del mapa
    min_lat, max_lat = 6.225, 6.235
    min_lon, max_lon = -73.395, -73.385

    x = img_width * (lon - min_lon) / (max_lon - min_lon)
    y = img_height * (max_lat - lat) / (max_lat - min_lat)
    return int(x), int(y)

# Función para mostrar estaciones aleatorias en una nueva ventana
def mostrar_estaciones_aleatorias():
    estaciones_aleatorias = random.sample(lista_estaciones, 3)

    nueva_ventana = Toplevel(root)
    nueva_ventana.title("Estaciones de Carga Cercanas")

    # Cargar la imagen del mapa
    mapa_img = Image.open("mapa_bolivar.png")  # Ruta de la imagen del mapa
    mapa_tk = ImageTk.PhotoImage(mapa_img)
    img_width, img_height = mapa_img.size

    canvas = Canvas(nueva_ventana, width=img_width, height=img_height)
    canvas.pack()

    # Mostrar el mapa en el canvas
    canvas.create_image(0, 0, anchor=NW, image=mapa_tk)

    # Dibujar los puntos de las estaciones
    for estacion in estaciones_aleatorias:
        nombre, lat, lon = estacion
        x, y = lat_lon_to_pixel(lat, lon, img_width, img_height)

        # Dibujar un punto en la ubicación calculada
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")  # Tamaño del punto

        # Añadir una etiqueta encima del punto
        canvas.create_text(x, y - 10, text=nombre, fill="black", font=("Arial", 10))

    # Mantener la referencia de la imagen para que se muestre correctamente
    canvas.image = mapa_tk

# Función para registrar usuario
def registrar():
    nombre = nombreEntry.get()
    contra = passEntry.get()

    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, contra) VALUES (%s, %s)", (nombre, contra))
        conexion.commit()
        messagebox.showinfo("Registro", f"Usuario '{nombre}' registrado con éxito.")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error de Registro", f"El usuario '{nombre}' ya existe.")
    finally:
        cursor.close()

# Interfaz gráfica con Tkinter
root = Tk()
root.title("Login Usuario")

mainFrame = Frame(root)
mainFrame.pack()
mainFrame.config(width=480, height=320, bg="lightblue")

titulo = Label(mainFrame, text="Login De Usuario ElectricWorld", font=("Arial", 24))
titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

nombreLabel = Label(mainFrame, text="Nombre:")
nombreLabel.grid(column=0, row=1, padx=10, pady=10, sticky="e")

nombreEntry = Entry(mainFrame)
nombreEntry.grid(column=1, row=1, padx=10, pady=10)

passLabel = Label(mainFrame, text="Contraseña:")
passLabel.grid(column=0, row=2, padx=10, pady=10, sticky="e")

passEntry = Entry(mainFrame, show="*")
passEntry.grid(column=1, row=2, padx=10, pady=10)

loginButton = Button(mainFrame, text="Login", width=10, command=conectar)
loginButton.grid(column=1, row=3, pady=10)

registrarButton = Button(mainFrame, text="Registrar", width=10, command=registrar)
registrarButton.grid(column=1, row=4, pady=10)

root.mainloop()

conexion.close()