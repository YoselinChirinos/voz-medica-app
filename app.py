from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'voz_medica_segura_2026' 

PASSWORD_DOCTOR = "medico20262620" 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD_DOCTOR:
            session.permanent = True
            session['doctor_auth'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error="Clave incorrecta")
    return render_template('login.html')

@app.route('/')
def index():
    if not session.get('doctor_auth'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
