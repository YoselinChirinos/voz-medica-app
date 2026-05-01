from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = "clave_fija_para_tu_tesis_2026" # Cambia esto si deseas

# SEGURIDAD: Datos de acceso
PASSWORD_DOCTOR = "medico20262620"

# CONEXIÓN SUPABASE (Verifica que estos datos sean los de tu proyecto actual)
SUPABASE_URL = "https://gzlccjdaxdxrrbaqemgo.supabase.co"
SUPABASE_KEY = "sb_publishable_Qtzr0MnVTUuMa2_1KoEpFg_bomVqHXI"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD_DOCTOR:
            session['autenticado'] = True
            return redirect(url_for('index'))
    return '''
        <body style="background:#f4f7f6; font-family:sans-serif; text-align:center; padding-top:100px;">
            <form method="post" style="background:white; display:inline-block; padding:40px; border-radius:10px; border:1px solid #ddd;">
                <h2>🔒 Acceso Médico</h2>
                <input type="password" name="password" placeholder="Contraseña" required style="padding:10px; margin-bottom:10px;"><br>
                <button type="submit" style="background:#e74c3c; color:white; border:none; padding:10px 20px; cursor:pointer;">ENTRAR</button>
            </form>
        </body>
    '''

@app.route('/')
def index():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    if not session.get('autenticado'):
        return jsonify({"status": "error"}), 401
    try:
        data = request.json
        supabase.table('consultas').insert(data).execute()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)