from googleapiclient.errors import HttpError
import io
from googleapiclient.http import MediaIoBaseDownload

def extract_text(service, file_item):
    """Extrae texto del archivo para análisis."""
    try:
        mime_type = file_item.get('mimeType', '')
        file_id = file_item['id']
        
        # Google Docs - Exportar como texto plano
        if mime_type == 'application/vnd.google-apps.document':
            request = service.files().export_media(
                fileId=file_id,
                mimeType='text/plain'
            )
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            return file_content.getvalue().decode('utf-8')
        
        # Google Sheets - Exportar como CSV
        elif mime_type == 'application/vnd.google-apps.spreadsheet':
            request = service.files().export_media(
                fileId=file_id,
                mimeType='text/csv'
            )
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            return file_content.getvalue().decode('utf-8')
        
        # Archivos de texto plano
        elif mime_type.startswith('text/'):
            request = service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            return file_content.getvalue().decode('utf-8', errors='ignore')
        
        # PDFs y otros archivos - solo usar el nombre
        else:
            return file_item.get('name', '')
            
    except Exception as e:
        print(f"   ⚠️  No se pudo extraer contenido, usando solo nombre del archivo")
        return file_item.get('name', '')

def get_or_create_folder(service, folder_name, parent_id=None):
    """
    Busca una carpeta por nombre, o la crea si no existe.
    Retorna el ID de la carpeta.
    """
    try:
        # Buscar si la carpeta ya existe
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        folders = results.get('files', [])
        
        if folders:
            print(f"📁 Carpeta '{folder_name}' ya existe")
            return folders[0]['id']
        
        # Crear la carpeta si no existe
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()
        
        print(f"✅ Carpeta '{folder_name}' creada")
        return folder['id']
        
    except HttpError as error:
        print(f"❌ Error creando carpeta '{folder_name}': {error}")
        return None

def move_file_to_folder(service, file_id, folder_id, file_name):
    """
    Mueve un archivo a una carpeta específica.
    """
    try:
        # Obtener los padres actuales del archivo
        file = service.files().get(
            fileId=file_id,
            fields='parents'
        ).execute()
        
        previous_parents = ",".join(file.get('parents', []))
        
        # Mover el archivo
        service.files().update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        
        print(f"   ✅ Movido a carpeta")
        return True
        
    except HttpError as error:
        print(f"   ❌ Error moviendo archivo: {error}")
        return False