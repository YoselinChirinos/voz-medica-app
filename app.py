from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)

# CONFIGURACIÓN DE SEGURIDAD
# Esta clave cifra la sesión; puedes poner cualquier frase larga
app.secret_key = 'clave_secreta_para_tesis_yoselin' 

# Esta es la contraseña que le darás al doctor
PASSWORD_DOCTOR = "medico20262620" 

# CONFIGURACIÓN DE SUPABASE
# Asegúrate de que estas URL y KEY sean las que copiaste de tu panel de Supabase
SUPABASE_URL = "https://gzlccjdaxdxrrbaqemgo.supabase.co"
SUPABASE_KEY = "sb_publishable_Qtzr0MnVTUuMa2_1KoEpFg_bomVqHXI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- RUTAS DE ACCESO Y SEGURIDAD ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verificamos si la clave escrita es la correcta
        if request.form.get('password') == PASSWORD_DOCTOR:
            session['autenticado'] = True
            return redirect(url_for('index'))
        else:
            return "Contraseña incorrecta. Intenta de nuevo."
            
    # Formulario sencillo de login (puedes luego ponerle CSS para que se vea pro)
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

# --- RUTA PRINCIPAL (PROTEGIDA) ---

@app.route('/')
def index():
    # Si NO está autenticado, lo mandamos al login
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('index.html')

# --- RUTA PARA GUARDAR DATOS EN SUPABASE ---

@app.route('/guardar', methods=['POST'])
def guardar_datos():
    if not session.get('autenticado'):
        return jsonify({"status": "error", "message": "No autorizado"}), 401

    try:
        data = request.json
        dictado = data.get('texto')

        if not dictado:
            return jsonify({"status": "error", "message": "No hay texto para guardar"}), 400

        # Insertamos en la tabla 'consultas' (asegúrate que se llame así en Supabase)
        response = supabase.table('consultas').insert({"dictado": dictado}).execute()

        return jsonify({"status": "success", "message": "Consulta guardada exitosamente en Supabase"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)