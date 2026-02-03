# Script para probar qué modelos de Gemini están disponibles
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Listando modelos disponibles...\n")
try:
    models = client.models.list()
    for model in models:
        print(f"Modelo: {model.name}")
        print(f"  Descripción: {getattr(model, 'description', 'N/A')}")
        print(f"  Capacidades: {getattr(model, 'supported_generation_methods', 'N/A')}")
        print()
except Exception as e:
    print(f"Error al listar modelos: {e}")
