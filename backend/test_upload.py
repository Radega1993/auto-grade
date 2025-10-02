import requests
import json

# Crear un archivo de prueba
test_content = """Ejercicio 1: Resuelve la ecuación 2x + 5 = 13

Ejercicio 2: Calcula el área de un triángulo con base 8 cm y altura 6 cm

Ejercicio 3: Simplifica la expresión: 3x + 2x - 5x + 7

Ejercicio 4: Encuentra el valor de x en la ecuación: x² - 9 = 0

Ejercicio 5: Resuelve el sistema de ecuaciones:
2x + y = 7
x - y = 2"""

with open('test_assignment.txt', 'w') as f:
    f.write(test_content)

print("Archivo de prueba creado: test_assignment.txt")
print("Contenido:")
print(test_content)
print("\n" + "="*50)
print("Para probar la funcionalidad completa:")
print("1. Ve a http://localhost:3000")
print("2. Usa las credenciales: admin@autograder.com / Admin123!")
print("3. Haz clic en 'Crear Solución y Rúbrica'")
print("4. Sube el archivo test_assignment.txt")
print("5. El sistema procesará el archivo con IA")
