from flask import Blueprint, render_template, request, redirect, url_for
from models.user_model import UserModel
import pusher

user_routes = Blueprint("user_routes", __name__)

# Instancia del modelo
user_model = UserModel()

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id='1767934',
    key='ffa9ea426828188c22c1',
    secret='628348e447718a9eec1f',
    cluster='us2',
    ssl=True
)

@user_routes.route("/")
def index():
    usuarios = user_model.obtener_usuarios()
    return render_template("app.html", usuarios=usuarios)

@user_routes.route("/usuarios/guardar", methods=["POST"])
def usuarios_guardar():
    usuario = request.form["txtUsuario"]
    contrasena = request.form["txtContrasena"]

    user_model.guardar_usuario(usuario, contrasena)

    # Notificar mediante Pusher
    pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {
        "usuario": usuario,
        "contrasena": contrasena
    })

    return redirect(url_for("user_routes.index"))

@user_routes.route("/usuarios/actualizar/<int:id>", methods=["POST"])
def usuarios_actualizar(id):
    usuario = request.form["txtUsuario"]
    contrasena = request.form["txtContrasena"]

    user_model.actualizar_usuario(id, usuario, contrasena)
    return redirect(url_for("user_routes.index"))

@user_routes.route("/usuarios/eliminar/<int:id>", methods=["POST"])
def usuarios_eliminar(id):
    user_model.eliminar_usuario(id)
    return redirect(url_for("user_routes.index"))
