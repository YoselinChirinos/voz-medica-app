from flask import Flask, render_template, request, jsonify, send_from_directory
from fpdf import FPDF
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN DE LA BASE DE DATOS (SUPABASE) ---
# Reemplaza TU_CONTRASEÑA_REAL con la clave que definiste en Supabase
DB_URI = "postgresql://postgres:Jsmch1610$princesa@db.gzlccjdaxdxrrbaqemgo.supabase.co:5432/postgres"

# Carpeta para guardar los PDFs temporales
PDF_FOLDER = "static/pdfs"
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar_consulta', methods=['POST'])
def guardar_consulta():
    try:
        datos = request.json
        # Conexión a la base de datos en la nube
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        
        # Insertar los datos en la tabla 'consultas'
        # Usamos .get() para evitar errores si algún campo viene vacío
        cur.execute(
            """INSERT INTO consultas 
               (nombre_paciente, cedula, informe, recipe, indicaciones, examenes) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                datos.get('paciente_nombre'), 
                datos.get('cedula'), 
                datos.get('informe'), 
                datos.get('recipe'), 
                datos.get('indicaciones'), 
                datos.get('examenes')
            )
        )
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "✅ Consulta guardada en Supabase exitosamente"})
    except Exception as e:
        print(f"Error de base de datos: {e}")
        return jsonify({"mensaje": f"❌ Error al conectar con la nube: {str(e)}"}), 500

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    try:
        datos = request.json
        nombre_archivo = f"orden_{datos.get('cedula', 'sin_cedula')}.pdf"
        ruta_pdf = os.path.join(PDF_FOLDER, nombre_archivo)
        
        pdf = FPDF()
        
        # Función interna para crear cada una de las 4 hojas con el mismo encabezado
        def agregar_hoja(titulo_hoja, contenido):
            pdf.add_page()
            # Encabezado unificado
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(2, 119, 189) # Azul profesional
            pdf.cell(0, 10, titulo_hoja, ln=True, align='C')
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 8, f"Paciente: {datos.get('paciente_nombre')} | C.I: {datos.get('cedula')}", ln=True)
            pdf.cell(0, 8, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(10)
            
            # Contenido de la hoja
            pdf.set_font("Arial", size=11)
            # Aseguramos compatibilidad de caracteres para evitar signos de interrogación
            texto_seguro = contenido.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 8, texto_seguro)

        # Generar las 4 hojas requeridas
        agregar_hoja("Informe Clínico", datos.get('informe', ''))
        agregar_hoja("Récipe Médico", datos.get('recipe', ''))
        agregar_hoja("Indicaciones al Paciente", datos.get('indicaciones', ''))
        agregar_hoja("Orden para Exámenes de Laboratorio y Otros", datos.get('examenes', ''))
        
        pdf.output(ruta_pdf)
        return jsonify({"url": f"/static/pdfs/{nombre_archivo}"})
    except Exception as e:
        print(f"Error PDF: {e}")
        return jsonify({"mensaje": "Error al generar el PDF"}), 500

if __name__ == '__main__':
    app.run(debug=True)