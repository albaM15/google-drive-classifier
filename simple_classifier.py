# Clasificador Simple Basado en Reglas (Sin IA)
# Este clasificador funciona sin necesidad de API de Gemini

import re
from typing import Dict

def classify_content_simple(text: str, filename: str) -> str:
    """
    Clasifica archivos basándose en palabras clave y nombres de archivo.
    No requiere API de IA.
    """
    if not text or len(text.strip()) < 10:
        return "Varios"
    
    # Combinar el nombre del archivo y contenido para análisis
    content_lower = (filename + " " + text).lower()
    
    # Palabras clave por categoría
    keywords = {
        "Universidad": [
            "examen", "tarea", "laboratorio", "informe", "proyecto",
            "universidad", "upao", "curso", "estudiante", "profesor",
            "investigación", "legal", "derecho", "sunat", "fiscal",
            "lab", "trabajo", "calificación", "semestre"
        ],
        "Backend": [
            "python", "java", "api", "server", "database", "sql",
            "nodejs", "django", "flask", "endpoint", "microservice",
            "rest", "graphql", "authentication", "authorization"
        ],
        "Frontend": [
            "react", "vue", "angular", "html", "css", "javascript",
            "component", "ui", "interface", "responsive", "tailwind",
            "bootstrap", "dom", "browser"
        ],
        "Finanzas": [
            "factura", "pago", "presupuesto", "dinero", "banco",
            "inversión", "gasto", "ingreso", "contabilidad", "precio",
            "costo", "económico", "financiero"
        ],
        "Personal": [
            "receta", "cocina", "viaje", "familia", "foto", "video",
            "personal", "privado", "cumpleaños", "vacaciones"
        ]
    }
    
    # Contar coincidencias por categoría
    scores: Dict[str, int] = {category: 0 for category in keywords}
    
    for category, words in keywords.items():
        for word in words:
            # Buscar palabra completa (no subcadenas)
            if re.search(r'\b' + re.escape(word) + r'\b', content_lower):
                scores[category] += 1
    
    # Obtener la categoría con mayor puntuación
    max_score = max(scores.values())
    
    if max_score == 0:
        return "Varios"
    
    # Retornar la categoría con mayor coincidencias
    for category, score in scores.items():
        if score == max_score:
            return category
    
    return "Varios"
