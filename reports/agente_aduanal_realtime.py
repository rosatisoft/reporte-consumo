import google.generativeai as genai
import pandas as pd
import json
from lector import get_emails 

# CONFIGURACIÓN PRO
API_KEY = "TU_NUEVA_KEY" # Asegúrate de poner la nueva aquí
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')

def agente_aduanal_pro():
    print("--- 1. Escaneando Bandeja Corporativa ---")
    correos = get_emails() 
    
    # Tomamos los últimos 20 para el demo para asegurar velocidad y cuota
    bloque_correos = "\n".join(correos[:20])

    prompt = f"""
    Eres un Agente de Inteligencia Aduanal experto. Analiza estos correos y genera una tabla de operaciones.
    
    CATEGORÍAS:
    - DOCUMENTACIÓN: Facturas, Pedimentos, BL.
    - OPERATIVO: Reportes de patio, estatus de maniobras.
    - COMERCIAL: Solicitudes de servicio, cotizaciones.
    - RIESGO: Phishing, Spam o discrepancias en documentos.

    EXTRAE SIEMPRE: ID_Op (Busca números de referencia o pedimentos), Emisor, Asunto, Monto, Urgencia (Alta/Media/Baja) y Es_Phishing (True/False).
    
    CORREOS:
    {bloque_correos}

    RESPONDE EXCLUSIVAMENTE EN FORMATO JSON (una lista de objetos):
    [{{"ID_Op": "Ref-123", "Categoria": "DOCUMENTACIÓN", "Emisor": "Nombre", "Asunto": "Texto", "Urgencia": "Alta", "Monto": "0.00", "Es_Phishing": false}}]
    """

    print("--- 2. IA Procesando Flujo de Aduanas ---")
    response = model.generate_content(prompt)
    
    # Limpiamos la respuesta para asegurar JSON puro
    raw_json = response.text.replace('```json', '').replace('```', '').strip()
    
    try:
        datos = json.loads(raw_json)
        df = pd.DataFrame(datos)
        
        # GUARDADO CRUCIAL: Esto es lo que el Dashboard lee
        df.to_csv("datos_dashboard.csv", index=False)
        print(f"✅ Reporte generado: {len(df)} operaciones actualizadas para el Dashboard.")
        
    except Exception as e:
        print(f"Error al procesar JSON: {e}")

if __name__ == "__main__":
    agente_aduanal_pro()
