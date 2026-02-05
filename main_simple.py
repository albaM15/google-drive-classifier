from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from drive_utils import extract_text, get_or_create_folder, move_file_to_folder
from simple_classifier import classify_content_simple
import config

def main():
    creds = Credentials.from_authorized_user_file('token.json', config.DRIVE_SCOPES)
    service = build('drive', 'v3', credentials=creds)

    # Obtener archivos del Drive
    results = service.files().list(
        q="mimeType != 'application/vnd.google-apps.folder' and trashed = false",
        pageSize=10, fields="files(id, name, mimeType)").execute()
    
    files = results.get('files', [])
    
    if not files:
        print("No se encontraron archivos en tu Google Drive.")
        return
    
    print("🗂️  Organizando archivos de Google Drive...\n")
    
    # Categorías disponibles
    categories = ["Backend", "Frontend", "Universidad", "Finanzas", "Personal", "Varios"]
    
    # Crear carpetas para cada categoría
    print("📁 Creando carpetas de categorías...\n")
    folder_ids = {}
    for category in categories:
        folder_id = get_or_create_folder(service, category)
        if folder_id:
            folder_ids[category] = folder_id
    
    print(f"\n🔍 Clasificando y moviendo {len(files)} archivo(s)...\n")
    
    # Contador de archivos movidos
    moved_count = 0
    
    # Clasificar y mover cada archivo
    for item in files:
        content = extract_text(service, item)
        category = classify_content_simple(content, item['name'])
        
        print(f"📄 {item['name']}")
        print(f"   └─ Categoría: {category}")
        
        # Mover archivo a su carpeta
        if category in folder_ids:
            success = move_file_to_folder(
                service, 
                item['id'], 
                folder_ids[category],
                item['name']
            )
            if success:
                moved_count += 1
        
        print()  # Línea en blanco para separar
    
    # Resumen final
    print("=" * 60)
    print(f"✅ Proceso completado!")
    print(f"📊 Archivos procesados: {len(files)}")
    print(f"📁 Archivos movidos: {moved_count}")
    print("=" * 60)
    

if __name__ == '__main__':
    main()
