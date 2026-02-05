#!/usr/bin/env python3
"""
Script de prueba para verificar que el clasificador funciona correctamente.
No requiere conexión a Google Drive.
"""

from simple_classifier import classify_content_simple

def test_classifier():
    """Prueba el clasificador con diferentes textos de ejemplo"""
    
    print("=" * 70)
    print("🧪 PRUEBA DEL CLASIFICADOR DE ARCHIVOS")
    print("=" * 70)
    print()
    
    # Casos de prueba
    test_cases = [
        {
            "name": "Informe_Lab_Fisica.txt",
            "content": "Este es el informe del laboratorio de física de la universidad UPAO. El experimento se realizó con el profesor García y se obtuvieron los siguientes resultados en el curso de Mecánica.",
            "expected": "Universidad"
        },
        {
            "name": "API_Documentation.txt",
            "content": "Esta es la documentación de la API REST del backend. El servidor utiliza Python con Flask y se conecta a una database SQL para authentication y authorization de usuarios.",
            "expected": "Backend"
        },
        {
            "name": "React_Component.js",
            "content": "import React from 'react'; const MyComponent = () => { return <div className='ui-container'>Hello World with Tailwind CSS</div>; };",
            "expected": "Frontend"
        },
        {
            "name": "Factura_Enero.pdf",
            "content": "Factura del banco por pago de servicios. Monto total: $500. Detalles de gastos e ingresos del mes. Contabilidad financiera.",
            "expected": "Finanzas"
        },
        {
            "name": "Receta_Pasta.txt",
            "content": "Receta de cocina para pasta carbonara. Ingredientes para la familia: huevos, queso, panceta. Perfecto para cumpleaños o vacaciones.",
            "expected": "Personal"
        },
        {
            "name": "Random_File.txt",
            "content": "Este es un archivo sin palabras clave específicas de ninguna categoría conocida.",
            "expected": "Varios"
        }
    ]
    
    # Ejecutar pruebas
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─' * 70}")
        print(f"Prueba {i}/{len(test_cases)}: {test['name']}")
        print(f"{'─' * 70}")
        print(f"Contenido: {test['content'][:80]}...")
        
        result = classify_content_simple(test['content'], test['name'], debug=True)
        
        if result == test['expected']:
            print(f"\n   ✅ CORRECTO - Clasificado como: {result}")
            passed += 1
        else:
            print(f"\n   ❌ ERROR - Esperado: {test['expected']}, Obtenido: {result}")
            failed += 1
    
    # Resumen
    print(f"\n{'=' * 70}")
    print(f"📊 RESUMEN DE PRUEBAS")
    print(f"{'=' * 70}")
    print(f"✅ Pasadas: {passed}/{len(test_cases)}")
    print(f"❌ Fallidas: {failed}/{len(test_cases)}")
    print(f"📈 Tasa de éxito: {(passed/len(test_cases)*100):.1f}%")
    print(f"{'=' * 70}\n")

if __name__ == '__main__':
    test_classifier()
