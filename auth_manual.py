# auth_manual.py
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/drive']

def generate_token():
    if not os.path.exists('credentials.json'):
        print("Error: No encuentro 'credentials.json'. Descárgalo de Google Cloud Console.")
        return
    
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    
    # Use manual copy-paste method instead of local server
    # This works better on headless systems or when browser integration fails
    try:
        creds = flow.run_console()  # This will give you a URL to visit manually
    except Exception as e:
        print(f"Error durante la autenticación: {e}")
        print("\nIntentando método manual...")
        # Get the authorization URL
        auth_url, _ = flow.authorization_url(prompt='consent')
        print(f"\n1. Visita esta URL en tu navegador:\n{auth_url}")
        print("\n2. Después de autorizar, copia el código que aparece")
        code = input("\n3. Pega el código aquí: ").strip()
        flow.fetch_token(code=code)
        creds = flow.credentials
    
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("¡Archivo token.json generado con éxito!")

if __name__ == '__main__':
    generate_token()
