from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from drive_utils import extract_text, move_file_to_folder
from ai_classifier import classify_content
import config

def main():
    creds = Credentials.from_authorized_user_file('token.json', config.DRIVE_SCOPES)
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q="mimeType != 'application/vnd.google-apps.folder' and trashed = false",
        pageSize=10, fields="files(id, name, mimeType)").execute()
    
    for item in results.get('files', []):
        content = extract_text(service, item)
        category = classify_content(content, item['name'])
        print(f"Archivo: {item['name']} -> Categoría: {category}")
    

if __name__ == '__main__':
    main()