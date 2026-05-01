from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)
# Genera una clave segura para las sesiones
app.secret_key = os.urandom(24)

# SEGURIDAD: Contraseña de acceso al sistema
PASSWORD_DOCTOR = "medico20262620"

# CONEXIÓN SUPABASE
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
    
    # Formulario de seguridad integrado
    return '''
        <div style="text-align:center; margin-top:100px; font-family:sans-serif;">
            <div style="display:inline-block; padding:50px; border:1px solid #ddd; border-radius:10px; background:white; shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h2>🔒 Acceso Médico Requerido</h2>
                <form method="post">
                    <input type="password" name="password" placeholder="Clave de Seguridad" required 
                           style="padding:15px; width:250px; margin-bottom:20px; border-radius:5px; border:1px solid #ccc;">
                    <br>
                    <button type="submit" style="padding:10px 30px; background:#e74c3c; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">ENTRAR</button>
                </form>
            </div>
        </div>
    '''

@app.route('/')
def index():
    # Si no ha iniciado sesión, no puede ver el panel médico
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar_datos():
    # Protección de la API: solo permite guardar si está autenticado
    if not session.get('autenticado'):
        return jsonify({"status": "error", "message": "No autorizado"}), 401
    
    try:
        data = request.json
        supabase.table('consultas').insert({
            "paciente": data.get('paciente'),
            "cedula": data.get('cedula'),
            "informe": data.get('informe'),
            "recipe": data.get('recipe'),
            "indicaciones": data.get('indicaciones'),
            "examenes": data.get('examenes')
        }).execute()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)