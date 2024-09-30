from flask import Flask
from flask import render_template
from flask import request
import pusher
import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Ruta principal
@app.route("/")
def index():
    con.close()
    return render_template("app.html")

# Ruta para mostrar alumnos (GET)
@app.route("/alumnos")
def alumnos():
    con.close()
    return render_template("alumnos.html")

# Ruta para guardar alumnos (POST)
@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Ruta para buscar registros de sensor_log
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM sensor_log ORDER BY Id_Log DESC")
    registros = cursor.fetchall()
    
    con.close()
    return registros

# Ruta para registrar datos en la tabla sensor_log
@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO sensor_log (Temperatura, Humedad, Fecha_Hora) VALUES (%s, %s, %s)"
    val = (args["temperatura"], args["humedad"], datetime.datetime.now(pytz.timezone("America/Matamoros")))
    cursor.execute(sql, val)
    
    con.commit()
    con.close()

    pusher_client = pusher.Pusher(
        app_id="1714541",
        key="cda1cc599395d699a2af",
        secret="9e9c00fc36600060d9e2",
        cluster="us2",
        ssl=True
    )

    pusher_client.trigger("canalRegistrosTemperaturaHumedad", "registroTemperaturaHumedad", args)
    return args

# Ruta para registrar un nuevo usuario en tst0_usuarios
@app.route("/usuarios/registrar", methods=["POST"])
def registrarUsuario():
    args = request.form

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
    val = (args["nombre_usuario"], args["contrasena"])
    cursor.execute(sql, val)

    con.commit()
    con.close()
    return f"Usuario {args['nombre_usuario']} registrado exitosamente."

# Ruta para registrar una nueva reserva en tst0_reservas
@app.route("/reservas/registrar", methods=["POST"])
def registrarReserva():
    args = request.form

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
    val = (args["nombre_apellido"], args["telefono"], args["fecha"])
    cursor.execute(sql, val)

    con.commit()
    con.close()
    return f"Reserva para {args['nombre_apellido']} registrada exitosamente."

# Ruta para buscar todas las reservas
@app.route("/reservas/buscar")
def buscarReservas():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_reservas ORDER BY Id_Reserva DESC")
    registros = cursor.fetchall()

    con.close()
    return registros

# Ruta para registrar un nuevo contacto en tst0_contacto
@app.route("/contacto/registrar", methods=["POST"])
def registrarContacto():
    args = request.form

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO tst0_contacto (Correo_Electronico, Nombre, Asunto) VALUES (%s, %s, %s)"
    val = (args["correo_electronico"], args["nombre"], args["asunto"])
    cursor.execute(sql, val)

    con.commit()
    con.close()
    return f"Contacto de {args['nombre']} registrado exitosamente."

if __name__ == "__main__":
    app.run(debug=True)
