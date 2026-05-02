from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)
# Mantén tu clave secreta para la seguridad de la sesión
app.secret_key = 'clave_secreta_voz_medica_2026'

# SEGURIDAD EXIGIDA
PASSWORD_MEDICO = "medico20262620"

# CONFIGURACIÓN DE SUPABASE (Verificada con tu imagen)
SUPABASE_URL = "https://gzlccjdaxdxrrbaqemgo.supabase.co"
SUPABASE_KEY = "sb_publishable_Qtzr0MnVTUuMa2_1KoEpFg_bomVqHXI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD_MEDICO:
            session.permanent = True
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
        return jsonify({"status": "error", "message": "Acceso denegado"}), 401
    
    try:
        data = request.json
        # MAPEADO EXACTO SEGÚN TU IMAGEN DE SUPABASE
        registro = {
            "nombre_paciente": data.get('nombre'), # Coincide con tu tabla
            "cedula": data.get('cedula'),          # Coincide con tu tabla
            "informe": data.get('informe'),        # Coincide con tu tabla
            "recipe": data.get('recipe'),          # Coincide con tu tabla
            "indicaciones": data.get('indicaciones'), # Coincide con tu tabla
            "examenes": data.get('examenes')       # Coincide con tu tabla (sin acento)
        }
        
        # Insertar en la tabla 'consultas'
        supabase.table('consultas').insert(registro).execute()
        return jsonify({"status": "success"}), 200

    except Exception as e:
        # Esto te dirá el error exacto en los logs de Render
        print(f"Error técnico: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)