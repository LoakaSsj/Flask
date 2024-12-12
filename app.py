from flask import Flask, render_template
from controllers.user_controller import user_routes

app = Flask(__name__)

# Registrar las rutas de usuarios
app.register_blueprint(user_routes)

if __name__ == "__main__":
    app.run(debug=True)
