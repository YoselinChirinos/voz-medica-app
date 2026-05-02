from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = 'clave_secreta_voz_medica_2026'

# SEGURIDAD: Acceso médico
PASSWORD_MEDICO = "medico20262620"

# CREDENCIALES (Verifica que sea la llave 'anon public')
SUPABASE_URL = "https://gzlccjdaxdxrrbaqemgo.supabase.co"
SUPABASE_KEY = "sb_publishable_Qtzr0MnVTUuMa2_1KoEpFg_bomVqHXL"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD_MEDICO:
            session['autenticado'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error="Contraseña incorrecta")
    return render_template('login.html')

@app.route('/')
def index():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar_datos():
    if not session.get('autenticado'):
        return jsonify({"status": "error", "message": "No autorizado"}), 401
    try:
        data = request.json
        registro = {
            "nombre_paciente": data.get('nombre'),
            "cedula": data.get('cedula'),
            "informe": data.get('informe'),
            "recipe": data.get('recipe'),
            "indicaciones": data.get('indicaciones'),
            "examenes": data.get('examenes')
        }
        # Intento de inserción
        res = supabase.table('consultas').insert(registro).execute()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        # Esto captura el error 401 y lo muestra amigablemente
        return jsonify({"status": "error", "message": str(e)}), 401

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)