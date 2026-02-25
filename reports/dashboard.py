import google.generativeai as genai
import pandas as pd
import json
from lector import get_emails # Tu extractor ya probado

# CONFIGURACIÓN PRO
API_KEY = "tu API_KREY aqui"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')

def agente_aduanal_pro():
    print("--- 1. Escaneando Bandeja Corporativa ---")
    correos = get_emails() # Recuerda borrar token.json para usar la cuenta nueva
    
    prompt = f"""
    Eres un Agente de Inteligencia Aduanal. Analiza estos correos y genera una tabla de operaciones.
    
    CATEGORÍAS:
    - DOCUMENTACIÓN: Facturas, Pedimentos, BL.
    - OPERATIVO: Reportes de patio, estatus de maniobras.
    - COMERCIAL: Solicitudes de servicio, cotizaciones.
    - RIESGO: Phishing, Spam o discrepancias en documentos.

    EXTRAE SIEMPRE: ID de Operación, Emisor, Monto (si aplica), y Urgencia (Alta/Media/Baja).
    
    CORREOS:
    {"\n".join(correos[:20])}

    RESPONDE SOLO EN JSON:
    [{{"ID_Op": "", "Categoria": "", "Estatus": "", "Urgencia": "", "Monto": "", "Es_Phishing": bool}}]
    """

    response = model.generate_content(prompt)
    # Lógica para guardar en Excel como hicimos antes...
    print("Reporte generado para el Dashboard.")

if __name__ == "__main__":
    agente_aduanal_pro()
