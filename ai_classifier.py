import requests
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def classify_content(text, filename):
    if not text or len(text.strip()) < 10:
        return "Varios"

    prompt = f"Analiza el archivo '{filename}' con este contenido: {text[:2000]}. Clasifica en: [Backend, Frontend, Universidad, Finanzas, Personal]. Responde solo la categoría."
    
    try:
        # Usar la API REST directamente
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            print(f"Error IA: {response.status_code} - {response.text}")
            return "Sin_Clasificar"
            
    except Exception as e:
        print(f"Error IA: {e}")
        return "Sin_Clasificar"