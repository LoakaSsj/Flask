from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime
import pytz
import pusher

# Configuración de la base de datos y Pusher (reemplaza con tus datos)
DATABASE_HOST = "185.232.14.52"
DATABASE_NAME = "u760464709_tst_sep"
DATABASE_USER = "u760464709_tst_sep_usr"
DATABASE_PASSWORD = "dJ0CIAFF="

PUSHER_APP_ID = '1768024'
PUSHER_KEY = '25ef14f3e9a47c712e61'
PUSHER_SECRET = '31c5ddebc75a9419e7d2'
PUSHER_CLUSTER = 'us2'

app = Flask(__name__)

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DATABASE_HOST,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )
        return connection
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos:", err)
        return None

def close_connection(connection):
    if connection:
        connection.close()

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/reservas")
def reservas():
    connection = get_connection()
    if not connection:
        return "Error al conectar a la base de datos!", 500

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tst0_reservas ORDER BY Id_Reserva DESC")
    reservas = cursor.fetchall()

    close_connection(connection)
    return render_template("alumnos.html", reservas=reservas)

@app.route("/reservas/guardar", methods=["POST"])
def reservas_guardar():
    nombre_apellido = request.form["txtNombreApellido"]
    telefono = request.form["txtTelefono"]

    connection = get_connection()
    if not connection:
        return "Error al conectar a la base de datos!", 500

    cursor = connection.cursor()
    fecha = datetime.datetime.now(pytz.timezone("America/Matamoros"))
    sql = "INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
    val = (nombre_apellido, telefono, fecha)
    cursor.execute(sql, val)
    connection.commit()

    # Evento Pusher
    pusher_client = pusher.Pusher(
        app_id=PUSHER_APP_ID,
        key=PUSHER_KEY,
        secret=PUSHER_SECRET,
        cluster=PUSHER_CLUSTER,
        ssl=True
    )
    pusher_client.trigger('reservas-channel', 'nueva-reserva', {
        'nombre_apellido': nombre_apellido,
        'telefono': telefono,
        'fecha': fecha.strftime("%Y-%m-%d %H:%M:%S")
    })

    close_connection(connection)

    return redirect(url_for("reservas"))

@app.route("/reservas/editar/<int:reserva_id>", methods=["GET", "POST"])
def reservas_editar(reserva_id):
    connection = get_connection()
    if not connection:
        return "Error al conectar a la base de datos!", 500

    cursor = connection.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM tst0_reservas WHERE Id_Reserva = %s", (reserva_id,))
        reserva = cursor.fetchone()
        if not reserva:
            return "Reserva no encontrada!", 404
        return render_template("alumnos.html", reserva=reserva, edit_mode=True)
    else:
        nombre_apellido = request.form["txtNombreApellido"]
        telefono = request.form["txtTelefono"]
        sql = "UPDATE tst0_reservas SET Nombre_Apellido = %s, Telefono = %s WHERE Id_Reserva = %s"
        val = (nombre_apellido, telefono, reserva_id)
        cursor.execute(sql, val)
        connection.commit()

        close_connection(connection)

        return redirect(url_for("reservas"))

@app.route("/reservas/eliminar/<int:reserva_id>", methods=["POST"])
def reservas_eliminar(reserva_id):
    connection = get_connection()
    if not connection:
        return "Error al conectar a la base de datos!", 500

    cursor = connection.cursor()
    sql = "DELETE FROM tst0_reservas WHERE Id_Reserva = %s"
    cursor.execute(sql, (reserva_id,))
    connection.commit()

    close_connection(connection)

    return redirect(url_for("reservas"))

if __name__ == "__main__":
    app.run(debug=True)
   
