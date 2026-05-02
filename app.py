from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS #
import os
from supabase import create_client, Client

app = Flask(__name__)
CORS(app) # Permite la conexión desde el navegador sin errores

# CONFIGURACIÓN DE SEGURIDAD (Mantenemos tus claves)
app.secret_key = 'clave_secreta_para_tesis_yoselin' 
PASSWORD_DOCTOR = "medico20262620" 

# CONFIGURACIÓN DE SUPABASE
SUPABASE_URL = "https://gzlccjdaxdxrrbaqemgo.supabase.co"
SUPABASE_KEY = "sb_publishable_Qtzr0MnVTUuMa2_1KoEpFg_bomVqHXI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD_DOCTOR:
            session['autenticado'] = True
            return redirect(url_for('index'))
        else:
            return "Contraseña incorrecta. Intenta de nuevo."
    return render_template('login.html') # O el bloque HTML que prefieras

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
        # Insertamos en tu tabla de Supabase con los nombres correctos
        supabase.table('consultas').insert({
            "nombre": data.get('nombre'),
            "cedula": data.get('cedula'),
            "telefono": data.get('telefono'),
            "informe": data.get('informe'),
            "recipe": data.get('recipe'),
            "indicaciones": data.get('indicaciones'),
            "examenes": data.get('examenes'),
            "proxima_cita": data.get('cita')
        }).execute()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Configuración esencial para Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)