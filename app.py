from flask import Flask, render_template, redirect, url_for, flash
from forms import ContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'

@app.route('/')
def index():
    form = ContactForm()  # Crea el formulario
    return render_template('index.html', form=form)  # Pasa el formulario a la plantilla

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash(f'Mensaje enviado por {form.name.data}!')
        return redirect(url_for('index'))  # Redirige a la página de inicio después de enviar el mensaje
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
