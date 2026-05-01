from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS  # Importante para evitar el error de conexión
import os
from supabase import create_client, Client

app = Flask(__name__)

# MEJORA: CORS permite que el navegador acepte la respuesta de Render
CORS(app)

# CONFIGURACIÓN DE SEGURIDAD
app.secret_key = 'clave_secreta_para_tesis_yoselin' 
PASSWORD_DOCTOR = "medico20262620" 

# CONFIGURACIÓN DE SUPABASE
SUPABASE_URL = "https://gzlccjdaxdxrrbaqemgo.supabase.co"
SUPABASE_KEY = "sb_publishable_Qtzr0MnVTUuMa2_1KoEpFg_bomVqHXI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- RUTAS DE ACCESO Y SEGURIDAD ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD_DOCTOR:
            session['autenticado'] = True
            return redirect(url_for('index'))
        else:
            return "Contraseña incorrecta. Intenta de nuevo."
            
    return '''
        <div style="text-align:center; margin-top:100px; font-family:Arial;">
            <h2 style="color:#2c3e50;">Voz Médica - Acceso Privado</h2>
            <p>Por favor, introduzca la clave de acceso para comenzar la prueba.</p>
            <form method="post">
                <input type="password" name="password" placeholder="Contraseña" style="padding:10px; width:200px;">
                <br><br>
                <button type="submit" style="padding:10px 20px; background-color:#3498db; color:white; border:none; border-radius:5px; cursor:pointer;">
                    Entrar al Sistema
                </button>
            </form>
        </div>
    '''

@app.route('/logout')
def logout():
    session.pop('autenticado', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('index.html')

# --- RUTA PARA GUARDAR DATOS MEJORADA ---

@app.route('/guardar', methods=['POST'])
def guardar_datos():
    # Verificación de seguridad por sesión
    if not session.get('autenticado'):
        return jsonify({"status": "error", "message": "No autorizado"}), 401

    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No se recibieron datos"}), 400

        # MEJORA: Mapeo de todos los campos que envía el nuevo index.html
        # Esto asegura que se guarde el informe, récipe, etc., en sus columnas
        response = supabase.table('consultas').insert({
            "nombre": data.get('nombre'),
            "cedula": data.get('cedula'),
            "telefono": data.get('telefono'),
            "informe": data.get('informe'),
            "recipe": data.get('recipe'),
            "indicaciones": data.get('indicaciones'),
            "examenes": data.get('examenes'),
            "proxima_cita": data.get('cita')
        }).execute()

        return jsonify({"status": "success", "message": "Consulta guardada exitosamente"}), 200
    
    except Exception as e:
        # Imprime el error en la consola de Render para que puedas verlo
        print(f"Error en Supabase: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # MEJORA: Configuración para que Render detecte el puerto automáticamente
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)