from flask import Flask
from flask import render_template
from flask import request
import pusher
import mysql.connector
import datetime
import pytz

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()
    return render_template("app.html")

# Ruta GET para mostrar la vista de alumnos
@app.route("/alumnos")
def alumnos():
    con.close()
    return render_template("alumnos.html")

# Ruta POST para guardar un alumno en la base de datos
@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Ruta para buscar registros de la tabla 'tst0_reservas'
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_reservas ORDER BY Id_Reserva DESC")
    registros = cursor.fetchall()

    con.close()
    return registros

# Ruta para registrar un nuevo valor en la tabla 'tst0_reservas'
@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()

    sql = "INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
    val = (args["nombre_apellido"], args["telefono"], datetime.datetime.now(pytz.timezone("America/Matamoros")))
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

    pusher_client.trigger("canalReservas", "nuevaReserva", args)

    return args

