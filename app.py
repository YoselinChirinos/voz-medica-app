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
            
    return '''
        <div style="text-align:center; margin-top:100px; font-family:Arial, sans-serif; background-color:#f4f7f6; height:100vh; padding-top:50px;">
            <div style="background:white; display:inline-block; padding:40px; border-radius:10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h2 style="color:#2c3e50;">Voz Médica - Acceso Privado</h2>
                <p style="color:#7f8c8d;">Introduzca la clave para comenzar la consulta</p>
                <form method="post">
                    <input type="password" name="password" placeholder="Contraseña" required 
                           style="padding:12px; width:250px; border:1px solid #bdc3c7; border-radius:5px; font-size:16px;">
                    <br><br>
                    <button type="submit" 
                            style="padding:12px 30px; background-color:#3498db; color:white; border:none; border-radius:5px; cursor:pointer; font-size:16px; font-weight:bold;">
                        Entrar al Sistema
                    </button>
                </form>
            </div>
        </div>
    '''

@app.route('/')
def index():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar_datos():
    if not session.get('autenticado'):
        return jsonify({"status": "error"}), 401
    try:
        data = request.json
        # Guardado completo en la tabla 'consultas'
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