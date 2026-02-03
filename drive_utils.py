import io
from googleapiclient.http import MediaIoBaseDownload

def extract_text(service, file):
    f_id = file['id']
    mime = file['mimeType']
    try:
        if 'vnd.google-apps.document' in mime:
            return service.files().export(fileId=f_id, mimeType='text/plain').execute().decode('utf-8')
        elif any(ext in mime for ext in ['json', 'javascript', 'text']):
            request = service.files().get_media(fileId=f_id)
            return request.execute().decode('utf-8')
    except:
        return ""
    return ""

def move_file_to_folder(service, file_id, folder_id):
    file = service.files().get(fileId=file_id, fields='parents').execute()
    prev_parents = ",".join(file.get('parents', []))
    service.files().update(fileId=file_id, addParents=folder_id, removeParents=prev_parents).execute()