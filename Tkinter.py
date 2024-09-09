
import mysql.connector
from tkinter import *
from tkinter import messagebox

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    user="root",
    host="localhost",
    database="proyecto_estaciones",
    port=3306
)

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
        buscar_estaciones()
    else:
        messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")

# Función para buscar estaciones de carga
def buscar_estaciones():
    ubicacion = input("Ingrese su ubicación actual (ciudad): ")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, direccion, precio FROM estaciones WHERE direccion LIKE %s", (f'%{ubicacion}%',))
    estaciones = cursor.fetchall()
    cursor.close()

    if estaciones:
        resultado = "Estaciones de carga encontradas:\n"
        for estacion in estaciones:
            nombre, direccion, precio = estacion
            resultado += f"- {nombre} en {direccion} (Precio: ${precio:.2f})\n"
        messagebox.showinfo("Estaciones Cercanas", resultado)
    else:
        messagebox.showinfo("Resultado de Búsqueda", "No se encontraron estaciones de carga cercanas.")

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

# Textos y títulos
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

# Botones de login y registro
loginButton = Button(mainFrame, text="Login", width=10, command=conectar)
loginButton.grid(column=1, row=3, pady=10)

registrarButton = Button(mainFrame, text="Registrar", width=10, command=registrar)
registrarButton.grid(column=1, row=4, pady=10)

root.mainloop()

conexion.close()