# --------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify
from flask import request
# Instalar con pip install flask-cors
from flask_cors import CORS
# Instalar con pip install mysql-connector-python
import mysql.connector
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename
# No es necesario instalar, es parte del sistema standard de Python
import os
import time
# --------------------------------------------------------------------

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas


class Catalogo:
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            dni INT,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            imagen_url VARCHAR(255))
            ''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    # ----------------------------------------------------------------
    def listar_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        usuarios = self.cursor.fetchall()
        return usuarios

    # ----------------------------------------------------------------
    def consultar_usuarios(self, dni):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM usuarios WHERE dni = {dni}")
        return self.cursor.fetchone()

    # ----------------------------------------------------------------
    def mostrar_usuarios(self, dni):
        # Mostramos los datos de un producto a partir de su código
        usuario = self.consultar_usuarios(dni)
        if usuario:
            print("-" * 40)
            print(f"DNI........: {usuario['dni']}")
            print(f"Nombre.....: {usuario['nombre']}")
            print(f"Apellido...: {usuario['apellido']}")
            print(f"Email......: {usuario['email']}")
            print(f"Imagen.....: {usuario['imagen_url']}")
            print("-" * 40)
        else:
            print("Usuario no encontrado.")

    # ----------------------------------------------------------------
    def agregar_usuario(self, dni, nombre, apellido, email, imagen):
        self.cursor.execute(f"SELECT * FROM usuarios WHERE dni = {dni}")
        usuario_existe = self.cursor.fetchone()
        if usuario_existe:
            return False

        sql = "INSERT INTO usuarios (dni, nombre, apellido, email, imagen_url) VALUES (%s, %s, %s, %s, %s)"
        valores = (dni, nombre, apellido, email, imagen)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True

    # ----------------------------------------------------------------
    def eliminar_usuario(self, dni):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM usuarios WHERE dni = {dni}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    # ----------------------------------------------------------------
    def modificar_usuario(self, dni, nuevo_nombre, nuevo_apellido, nuevo_email, nueva_imagen):
        sql = "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, imagen_url = %s WHERE dni = %s"
        valores = (nuevo_nombre, nuevo_apellido, nuevo_email, nueva_imagen, dni)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    # ----------------------------------------------------------------
    def obtener_nombre_imagen(self, dni):
        # Implementa la lógica para obtener la ruta de la imagen de un producto
        # a partir de su código. Devuelve la ruta completa de la imagen o None si no se encuentra.
        self.cursor.execute(f"SELECT imagen_url FROM usuarios WHERE dni = {dni}")
        resultado = self.cursor.fetchone()
        if resultado:
            return resultado['imagen_url']
        else:
            return None


# --------------------------------------------------------------------
# Cuerpo del programa
# --------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
catalogo = Catalogo(host='localhost', user='root', password='', database='miappp')

# Carpeta para guardar las imagenes
ruta_destino = 'static/img/'


# --------------------------------------------------------------------
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = catalogo.listar_usuarios()
    return jsonify(usuarios)


# --------------------------------------------------------------------
@app.route("/usuarios/<int:dni>", methods=["GET"])
def mostrar_usuarios(dni):
    catalogo.mostrar_usuarios(dni)
    usuario = catalogo.consultar_usuarios(dni)
    if usuario:
        return jsonify(usuario)
    else:
        return "Usuario no encontrado", 404


@app.route("/usuarios", methods=["POST"])
def agregar_usuario():
    # Recojo los datos del form
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    imagen = request.files['imagen']
    nombre_imagen = secure_filename(imagen.filename)

    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    imagen.save(os.path.join(ruta_destino, nombre_imagen))

    if catalogo.agregar_usuario(dni, nombre, apellido, email, nombre_imagen):
        return jsonify({"mensaje": "Usuario agregado"}), 201
    else:
        return jsonify({"mensaje": "Usuario ya existe"}), 400


@app.route("/usuarios/<int:dni>", methods=["DELETE"])
def eliminar_usuario(dni):
    # Primero, obtén la información del producto para encontrar la imagen
    usuario = catalogo.consultar_usuarios(dni)
    if usuario:
        # Eliminar la imagen asociada si existe
        ruta_imagen = os.path.join(ruta_destino, usuario['imagen_url'])
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el producto del catálogo
        if catalogo.eliminar_usuario(dni):
            return jsonify({"mensaje": "Usuario eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el usuario"}), 500
    else:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404


@app.route("/usuarios/<int:dni>", methods=["PUT"])
def modificar_usuario(dni):
    # Recojo los datos del form
    nuevo_nombre = request.form.get("nombre")
    nuevo_apellido = request.form.get("apellido")
    nuevo_email = request.form.get("email")

    # Verificar si se proporciona una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        nombre_imagen = secure_filename(imagen.filename)
        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        imagen.save(os.path.join(ruta_destino, nombre_imagen))
    else:
        # Si no se proporciona una nueva imagen, conservar la imagen existente
        nombre_imagen = catalogo.obtener_nombre_imagen(dni)

    # Actualización del producto
    if catalogo.modificar_usuario(dni, nuevo_nombre, nuevo_apellido, nuevo_email, nombre_imagen):
        return jsonify({"mensaje": "Usuario modificado"}), 200
    else:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
