# restfull_flask

# 🎮 API RESTful Flask – Gestión de Videojuegos

Proyecto desarrollado en **Flask** que permite gestionar videojuegos almacenados en una base de datos **MySQL**, con autenticación de usuarios, operaciones CRUD completas y documentación interactiva mediante **Swagger (Flasgger)**.

---

## 🚀 Características principales
- CRUD completo: crear, leer, actualizar y eliminar videojuegos.  
- Autenticación de usuarios con **Flask-Login** y **Werkzeug**.  
- Validación de formularios con **Flask-WTF**.  
- API RESTful documentada con **Flasgger / Swagger UI**.  
- Conexión a base de datos **MySQL** usando **SQLAlchemy** (ORM).  
- Estructura modular con **Blueprints** (`auth/` y `api/`).  

---

## 🗂️ Estructura del proyecto



flask_juegos/
│
├── api/ # Endpoints de la API REST
│ ├── init.py
│ └── routes.py
│
├── auth/ # Módulo de autenticación
│ ├── init.py
│ ├── forms.py
│ └── routes.py
│
├── static/ # Archivos CSS, JS, imágenes
├── templates/ # Vistas HTML
│
├── app2.py # Archivo principal de ejecución
├── bd.py # Configuración de la base de datos
├── controlador_juegos.py # Lógica CRUD con SQLAlchemy
├── forms.py # Formularios de Flask-WTF
├── models.py # Definición del modelo Juego y User
├── requirements.txt # Dependencias del proyecto
└── README.md


---

## ⚙️ Instalación y ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/navarro2020153/restfull_flask.git
cd restfull_flask


Crear entorno virtual e instalar dependencias
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


Configurar la base de datos MySQL

Edita la URI de conexión dentro de app2.py:

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/juegos'


Crea la base de datos “juegos” y ejecuta:

python app2.py
