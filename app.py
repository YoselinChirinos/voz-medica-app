from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = 'clave_secreta_voz_medica_2026'

# SEGURIDAD MANTENIDA
PASSWORD_MEDICO = "medico20262620"

# CONFIGURACIÓN DE SUPABASE
SUPABASE_URL = "https://gzlccjdaxdxrrbaqemgo.supabase.co"
# USA LA CLAVE ANON PUBLIC AQUÍ
SUPABASE_KEY = "sb_publishable_Qtzr0MnVTUuMa2_1KoEpFg_bomVqHXI"
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
        # IMPORTANTE: Estos nombres deben ser IGUALES a los de tu tabla en Supabase
        registro = {
            "nombre_paciente": data.get('nombre'),
            "cedula": data.get('cedula'),
            "informe": data.get('informe'),
            "recipe": data.get('recipe'),
            "indicaciones": data.get('indicaciones'),
            "examenes": data.get('examenes')
        }
        # Intentamos insertar en la tabla 'consultas'
        supabase.table('consultas').insert(registro).execute()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        # Esto nos dirá el error exacto en los logs de Render
        print(f"Error detectado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)