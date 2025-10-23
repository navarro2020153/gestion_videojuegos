from bd import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    @property
    def password(self):
        raise AttributeError('El password no es un atributo legible.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def verificar_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.username}>'


#MODELO DE JUEGO

class Juego(db.Model):
    __tablename__ = 'juegos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(150))
    precio = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<Juego {self.nombre}>'
