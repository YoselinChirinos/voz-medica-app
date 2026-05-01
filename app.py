from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.urandom(24)

# CONFIGURACIÓN DE SEGURIDAD
PASSWORD_DOCTOR = "medico20262620"

# CONFIGURACIÓN DE SUPABASE
SUPABASE_URL = "https://gzlccjdaxdxrrbaqemgo.supabase.co"
SUPABASE_KEY = "sb_publishable_Qtzr0MnVTUuMa2_1KoEpFg_bomVqHXI"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD_DOCTOR:
            session['autenticado'] = True
            return redirect(url_for('index'))
        else:
            return '<script>alert("Contraseña incorrecta"); window.location.href="/login";</script>'
    return render_template('login.html') # Asegúrate de tener este archivo o usa el HTML anterior

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
        # Inserción robusta en la tabla 'consultas'
        supabase.table('consultas').insert({
            "paciente": data.get('paciente', 'N/A'),
            "cedula": data.get('cedula', 'N/A'),
            "informe": data.get('informe', ''),
            "recipe": data.get('recipe', ''),
            "indicaciones": data.get('indicaciones', ''),
            "examenes": data.get('examenes', '')
        }).execute()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)