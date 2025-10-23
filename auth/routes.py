from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from . import auth
from .forms import LoginForm, RegisterForm
from models import db, User

#LOGIN
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Inicio de sesión exitoso. ¡Bienvenido!', 'success')
            return redirect(url_for('juegos'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

#REGISTRO
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
       
        nuevo_usuario = User(
            username=form.username.data,
            email=form.email.data
        )
        nuevo_usuario.password = form.password.data  

        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


#LOGOUT
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))
