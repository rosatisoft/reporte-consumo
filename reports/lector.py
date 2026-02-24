import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Permisos: Solo lectura para revisar correos
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_emails():
    creds = None
    # El archivo token.json guarda tus credenciales de usuario una vez que te logueas
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si no hay credenciales válidas, te pide loguearte
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para la próxima vez
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Conexión con el servicio de Gmail
    service = build('gmail', 'v1', credentials=creds)
    
    # Pedimos los últimos 100 mensajes
    results = service.users().messages().list(userId='me', maxResults=100).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No se encontraron correos.")
        return []

    print(f"Extrayendo información de {len(messages)} correos...")
    
    data_for_ai = []
    for msg in messages:
        try:
            m = service.users().messages().get(userId='me', id=msg['id'], format='metadata').execute()
            headers = m.get('payload', {}).get('headers', [])
            
            # Buscamos el Asunto y el Remitente de forma segura
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), "Sin Asunto")
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), "Desconocido")
            snippet = m.get('snippet', '')
            
            resumen = f"De: {sender} | Asunto: {subject} | Resumen: {snippet}"
            data_for_ai.append(resumen)
            print(f"- Leído: {subject[:50]}...") # Para ver progreso en consola
        except Exception as e:
            print(f"Error leyendo un correo: {e}")
            continue
    
    return data_for_ai

# --- ESTA ES LA PARTE QUE CORRE EL PROGRAMA ---
if __name__ == "__main__":
    lista_correos = get_emails()
    
    print("\n" + "="*50)
    print(f"PROCESO TERMINADO: Se obtuvieron {len(lista_correos)} correos.")
    print("="*50 + "\n")
    
    # Mostrar los primeros 5 como prueba
    for i, correo in enumerate(lista_correos[:5]):
        print(f"{i+1}. {correo}")
