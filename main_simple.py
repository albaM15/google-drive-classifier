from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from drive_utils import extract_text
from simple_classifier import classify_content_simple
import config

def main():
    creds = Credentials.from_authorized_user_file('token.json', config.DRIVE_SCOPES)
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q="mimeType != 'application/vnd.google-apps.folder' and trashed = false",
        pageSize=10, fields="files(id, name, mimeType)").execute()
    
    print("🗂️  Clasificando archivos de Google Drive (usando clasificador simple)...\n")
    
    for item in results.get('files', []):
        content = extract_text(service, item)
        category = classify_content_simple(content, item['name'])
        print(f"📄 {item['name']}")
        print(f"   └─ Categoría: {category}\n")
    

if __name__ == '__main__':
    main()
