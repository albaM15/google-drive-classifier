from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Nueva forma de inicializar el cliente
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def classify_content(text, filename):
    if not text or len(text.strip()) < 10:
        return "Varios"

    prompt = f"Analiza el archivo '{filename}' con este contenido: {text[:2000]}. Clasifica en: [Backend, Frontend, Universidad, Finanzas, Personal]. Responde solo la categoría."
    
    try:
        # Nueva sintaxis de generación
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error IA: {e}")
        return "Sin_Clasificar"