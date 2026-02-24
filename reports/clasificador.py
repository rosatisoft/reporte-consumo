import google.generativeai as genai
from lector import get_emails

# 1. Configuración de la IA
# Reemplaza 'TU_API_KEY' con la que obtuviste en AI Studio
genai.configure(api_key="TU_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def ejecutar_agente():
    print("--- 1. Extrayendo correos de Gmail ---")
    correos = get_emails()
    
    if not correos:
        print("No hay correos para analizar.")
        return

    # Unimos todos los correos en un solo bloque de texto
    texto_para_analizar = "\n".join(correos)

    # 2. El Prompt (Instrucciones maestras)
    prompt = f"""
    Eres un Agente de Inteligencia Operativa. Tu misión es clasificar estos 100 correos de la cuenta rosatisoft@gmail.com.
    
    CATEGORÍAS REQUERIDAS:
    1. FACTURAS/RECIBOS: Correos de Google Play, Render, Railway, etc. Extrae el monto si aparece en el resumen.
    2. IT/DESARROLLO: Notificaciones de GitHub, npm, fallos de despliegue (Railway/Render).
    3. SEGUIMIENTO/LOGÍSTICA: Cualquier número de guía o estatus de envío.
    4. VENTAS/MARKETING: eBay, Twilio, newsletters.
    5. ALERTAS DE SEGURIDAD: TeamViewer, Google Security, etc.

    DATOS A ANALIZAR:
    {texto_para_analizar}

    FORMATO DE SALIDA (Respuesta solo en este formato):
    ## REPORTE DE CLASIFICACIÓN
    **Resumen General:** (Escribe un breve análisis de la carga de trabajo actual).
    
    | Categoría | Asunto | Emisor | Detalle/Acción |
    | :--- | :--- | :--- | :--- |
    (Llena la tabla con los correos más relevantes)
    """

    print("--- 2. Gemini analizando y clasificando ---")
    response = model.generate_content(prompt)
    
    print("\n" + "="*60)
    print(response.text)
    print("="*60)

if __name__ == "__main__":
    ejecutar_agente()
