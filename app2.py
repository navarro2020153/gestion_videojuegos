from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required
from bd import db
import controlador_juegos
from forms import ContactForm
from models import User

# --- NUEVO: API REST y Swagger ---
from api import api_bp
from flasgger import Swagger

# --- Configuración principal ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_super_segura_2025'

# --- Inicializar base de datos ---
db.init_app(app)

# --- Configurar LoginManager ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Redirige al login si no está autenticado
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Importar y registrar Blueprint de autenticación ---
from auth import auth
app.register_blueprint(auth, url_prefix='/auth')

# --- REGISTRO DE API REST + SWAGGER ---
app.register_blueprint(api_bp)
Swagger(app, template={
    "swagger": "2.0",
    "info": {"title": "API Juegos", "version": "1.0.0"},
    "basePath": "/api"
})

# =========================
# RUTAS DEL PROYECTO (HTML)
# =========================

# Página principal con botones
@app.route("/")
def inicio():
    return redirect(url_for("juegos"))

@app.route("/juegos")
def juegos():
    return render_template("juegos.html")

# Página con tabla completa
@app.route("/listado_juegos")
@login_required
def listado_juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("listado_juegos.html", juegos=juegos)

# Buscar juego por ID
@app.route("/buscar_juego_por_id", methods=["POST"])
@login_required
def buscar_juego_por_id():
    id = request.form["id"]
    juego = controlador_juegos.obtener_juego_por_id(id)
    juegos = controlador_juegos.obtener_juegos()

    if juego:
        return render_template("listado_juegos.html", juego=juego, juegos=juegos)
    else:
        mensaje = f"No se encontró ningún juego con el ID {id}."
        return render_template("listado_juegos.html", mensaje=mensaje, juegos=juegos)

# Formulario para agregar juego
@app.route("/formulario_agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    return redirect(url_for("listado_juegos"))

# Formulario para editar juego
@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    return redirect(url_for("listado_juegos"))

# Eliminar juego
@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    id = request.form["id"]
    controlador_juegos.eliminar_juego(id)
    return redirect(url_for("listado_juegos"))

# Formulario de contacto
@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    form = ContactForm()
    if form.validate_on_submit():
        print("Mensaje recibido:", form.name.data, form.email.data, form.message.data)
        return redirect(url_for("juegos"))
    return render_template("contacto.html", form=form)

# =========================
# INICIALIZAR LA APLICACIÓN
# =========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8000)
