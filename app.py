from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import os
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# 1. SEGURIDAD: Configuración de sesión y clave del médico
app.secret_key = 'clave_secreta_para_tesis_yoselin' 
PASSWORD_DOCTOR = "medico20262620" 

# 2. CONEXIÓN: Datos de tu proyecto en Supabase
SUPABASE_URL = "https://gzlccjdaxdxrrbaqemgo.supabase.co"
SUPABASE_KEY = "sb_publishable_Qtzr0MnVTUuMa2_1KoEpFg_bomVqHXI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# RUTA: Pantalla de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD_DOCTOR:
            session['autenticado'] = True
            return redirect(url_for('index'))
        else:
            return "Contraseña incorrecta. Intente de nuevo."
    return render_template('login.html')

# RUTA: Consola de Dictado (Protegida)
@app.route('/')
def index():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('index.html')

# RUTA: Acción de Guardar en Supabase (Protegida)
@app.route('/guardar', methods=['POST'])
def guardar_datos():
    # Verificación de seguridad: solo si está logueado
    if not session.get('autenticado'):
        return jsonify({"status": "error", "message": "No autorizado"}), 401
    
    try:
        data = request.json
        
        # MAPEO EXACTO: Según tu imagen image_947f40.png
        # 'nombre_paciente' es la columna real en tu tabla
        registro = {
            "nombre_paciente": data.get('nombre'),
            "cedula": data.get('cedula'),
            "informe": data.get('informe'),
            "recipe": data.get('recipe'),
            "indicaciones": data.get('indicaciones'),
            "examenes": data.get('examenes')
        }
        
        # Ejecución del guardado en la nube
        # Nota: La columna 'fecha' se llena sola en Supabase
        supabase.table('consultas').insert(registro).execute()
        
        return jsonify({"status": "success"}), 200

    except Exception as e:
        # Si falla, el error aparecerá en el alert de tu pantalla
        print(f"Error de base de datos: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# CONFIGURACIÓN PARA RENDER
if __name__ == '__main__':
    # Render asigna un puerto dinámico, esto permite que la app lo detecte
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)