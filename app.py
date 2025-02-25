from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        recetas_file = request.files['recetas']
        ventas_file = request.files['ventas']
        
        if recetas_file and ventas_file:
            recetas_path = os.path.join(UPLOAD_FOLDER, recetas_file.filename)
            ventas_path = os.path.join(UPLOAD_FOLDER, ventas_file.filename)
            recetas_file.save(recetas_path)
            ventas_file.save(ventas_path)

            report_path = process_data(recetas_path, ventas_path)
            return render_template('result.html', report_path=f"/reports/{os.path.basename(report_path)}")
        else:
            return "Error: Debes subir ambos archivos."

    # Si la solicitud es GET, mostrar el formulario de subida
    return render_template('upload.html')

def process_data(recetas_path, ventas_path):
    ingredientes_df = pd.read_csv(recetas_path)
    ventas_df = pd.read_excel(ventas_path)
    
    ingredientes_df.columns = ["Producto", "Ingrediente", "Cantidad", "Unidad"]
    ingredientes_df = ingredientes_df.dropna()
    
    ventas_df = ventas_df.iloc[2:, [1, 3]]
    ventas_df.columns = ["Producto", "Cantidad Vendida"]
    ventas_df = ventas_df.dropna()
    ventas_df["Cantidad Vendida"] = pd.to_numeric(ventas_df["Cantidad Vendida"], errors="coerce")
    
    consumo_df = pd.merge(ingredientes_df, ventas_df, on="Producto", how="inner")
    consumo_df["Consumo Total"] = consumo_df["Cantidad"].astype(float) * consumo_df["Cantidad Vendida"].astype(float)
    
    consumo_total_df = consumo_df.groupby(["Ingrediente", "Unidad"])["Consumo Total"].sum().reset_index()
    report_filename = os.path.join(REPORTS_FOLDER, "reporte_consumo.xlsx")
    consumo_total_df.to_excel(report_filename, index=False)

    print(f"✅ Reporte generado en: {report_filename}")
    
    return report_filename
    
from flask import send_from_directory

@app.route('/reports/<filename>')
def serve_report(filename):
    return send_from_directory(REPORTS_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Usa el puerto que Render asigna
    app.run(host="0.0.0.0", port=port, debug=True)
