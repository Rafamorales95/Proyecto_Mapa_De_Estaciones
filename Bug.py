import sqlite3


# Clase Usuario
class Usuario:
    numUsuarios = 0

    def _init_(self, nombre, contra):
        self.nombre = nombre
        self.contra = contra
        self.conectado = False
        self.intentos = 3
        Usuario.numUsuarios += 1

    # Método para desconectar
    def desconectar(self):
        if self.conectado:
            print("¡Se cerró sesión con éxito!")
            self.conectado = False
        else:
            print("Error, no inició sesión.")

    # Representación en cadena del objeto
    def _str_(self):
        conect = "conectado" if self.conectado else "desconectado"
        return f"Mi nombre de usuario es {self.nombre} y estoy {conect}"

    # Método de clase para registrar un usuario en la base de datos
    @classmethod
    def registrar(cls):
        nombre = input("Ingrese su nombre de usuario: ")
        contra = input("Ingrese su contraseña: ")

        # Conectar a la base de datos SQLite
        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()

        # Crear la tabla si no existe
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          nombre TEXT NOT NULL UNIQUE,
                          contra TEXT NOT NULL)''')

        # Verificar si el usuario ya existe
        cursor.execute('SELECT * FROM usuarios WHERE nombre = ?', (nombre,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            print(f"El usuario '{nombre}' ya existe. No es posible registrar el usuario.")
        else:
            # Insertar el nuevo usuario
            cursor.execute('INSERT INTO usuarios (nombre, contra) VALUES (?, ?)', (nombre, contra))
            conexion.commit()
            print(f"Usuario '{nombre}' registrado con éxito.")

        # Cerrar la conexión a la base de datos
        conexion.close()


# Método para conectar un usuario
def conectar():
    nombre = input("Ingrese su nombre de usuario: ")
    contra = input("Ingrese su contraseña: ")

    # Conectar a la base de datos SQLite
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()

    # Buscar el usuario en la base de datos
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ? AND contra = ?', (nombre, contra))
    usuario_data = cursor.fetchone()

    conexion.close()

    # Verificar si se encontró el usuario
    if usuario_data:
        print("¡Usuario encontrado y contraseña correcta!")
        # Crear el objeto Usuario
        usuario = Usuario(nombre, contra)
        usuario.conectado = True  # Conectar automáticamente el usuario
        return usuario
    else:
        print("Usuario o contraseña incorrectos.")
        return None



def registrar():
    respuesta = input("Desea registrarse: ")

    if respuesta == "Si" or respuesta == "no":
        # Ejemplo de registro
        Usuario.registrar()
        return True
    else:
        print("Chao")
        return False
if registrar():
    conectar()
else:
    print("La Buenas Parcero")


