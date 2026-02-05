from googleapiclient.errors import HttpError
import io
from googleapiclient.http import MediaIoBaseDownload

def extract_text(service, file_item):
    """Extrae texto del archivo para análisis."""
    try:
        if 'google-apps' in file_item.get('mimeType', ''):
            if 'document' in file_item['mimeType']:
                return service.files().get(fileId=file_item['id'], fields='name').execute()['name']
        return file_item.get('name', '')
    except Exception as e:
        print(f"Error extrayendo texto: {e}")
        return ""

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