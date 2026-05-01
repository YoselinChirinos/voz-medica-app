from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = 'clave_secreta_tesis_yoselin'

# Credenciales
PASSWORD_DOCTOR = "medico20262620"
SUPABASE_URL = "https://gzlccjdaxdxrrbaqemgo.supabase.co"
SUPABASE_KEY = "sb_publishable_Qtzr0MnVTUuMa2_1KoEpFg_bomVqHXI"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD_DOCTOR:
            session['autenticado'] = True
            return redirect(url_for('index'))
    return render_template('login.html') # Asegúrate de tener login.html o usa el código anterior

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
        texto_dictado = data.get('texto')
        
        # 1. Guardar en Supabase
        supabase.table('consultas').insert({"dictado": texto_dictado}).execute()
        
        # 2. Responder al navegador para que el JS genere el PDF
        return jsonify({"status": "success", "message": "¡Datos guardados en la nube y listos para PDF!"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
