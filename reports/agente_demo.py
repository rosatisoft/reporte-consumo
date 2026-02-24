import google.generativeai as genai
import pandas as pd
import json
from lector import get_emails

# 1. CONFIGURACIÓN
API_KEY = "TU_API_KEY_AQUI" # Pon tu clave aquí
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def ejecutar_demo():
    print("--- 1. Extrayendo correos (Demo Mode) ---")
    correos = get_emails()
    
    if not correos:
        print("No hay correos.")
        return

    texto_para_analizar = "\n".join(correos)

    # 2. PROMPT AVANZADO PARA EXTRACCIÓN Y SEGURIDAD
    prompt = f"""
    Actúa como un Sistema de Triaje Inteligente. Analiza estos correos y clasifícalos.
    
    CRITERIOS DE SEGURIDAD Y PRIORIDAD:
    - Prioritarios: Facturas por pagar, errores de servidor críticos, o clientes directos.
    - Phishing/Basura: Correos con remitentes sospechosos o publicidad no solicitada.
    
    DATOS A EXTRAER:
    - Monto: Busca signos de $ o palabras como "Total", "Monto", "Neto".
    - Fecha: Fecha mencionada en el correo.
    - Emisor: Quién envía la factura o el aviso.
    - Cliente: A quién va dirigido (normalmente Ernesto o Rosatisoft).

    CORREOS:
    {texto_para_analizar}

    RESPONDE EXCLUSIVAMENTE EN FORMATO JSON (una lista de objetos) con estas llaves:
    "Categoria", "Prioridad", "Emisor", "Asunto", "Monto", "Fecha", "Es_Phishing", "Accion_Sugerida"
    """

    print("--- 2. Inteligencia Artificial analizando detalles financieros y seguridad ---")
    response = model.generate_content(prompt)
    
    # Limpiamos la respuesta para asegurarnos que sea JSON puro
    raw_json = response.text.replace('```json', '').replace('```', '').strip()
    
    try:
        datos = json.loads(raw_json)
        
        # 3. CREACIÓN DEL EXCEL
        df = pd.DataFrame(datos)
        
        # Ordenamos: Prioritarios arriba, Phishing abajo
        df['Prioridad_Num'] = df['Prioridad'].map({'Alta': 1, 'Media': 2, 'Baja': 3})
        df = df.sort_values(by=['Es_Phishing', 'Prioridad_Num'], ascending=[True, True])
        df = df.drop(columns=['Prioridad_Num'])

        nombre_archivo = "Reporte_Agente_IA.xlsx"
        df.to_excel(nombre_archivo, index=False)
        
        print(f"\n✅ ¡ÉXITO! Se ha generado el archivo: {nombre_archivo}")
        print(df[['Categoria', 'Prioridad', 'Emisor', 'Monto', 'Es_Phishing']].head(10))

    except Exception as e:
        print(f"Error al procesar el reporte: {e}")
        print("Respuesta cruda de la IA:", response.text)

if __name__ == "__main__":
    ejecutar_demo()
