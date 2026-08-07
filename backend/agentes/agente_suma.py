# backend/agentes/agente_suma.py
import time
import sys
import os

# Esto es un truco para que Python encuentre database.py en la carpeta anterior
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import registrar_operacion

def ejecutar_suma(num1: float, num2: float) -> float:
    """Agente especialista exclusivo para sumar."""
    print(f"➕ [Agente Suma] Activado: calculando {num1} + {num2}...")
    
    tiempo_inicio = time.time()
    
    try:
        resultado = num1 + num2
        estado = "exito"
        mensaje_error = None
    except Exception as e:
        resultado = None
        estado = "error"
        mensaje_error = str(e)
        
    # Calculamos los milisegundos que tardó
    tiempo_ms = int((time.time() - tiempo_inicio) * 1000)
    
    # El agente reporta su trabajo a PostgreSQL
    registrar_operacion(
        nombre_agente="agente_suma",
        peticion=f"{num1} + {num2}",
        respuesta=str(resultado),
        tiempo_ms=tiempo_ms,
        estado=estado,
        error=mensaje_error
    )
    
    return resultado

# --- BLOQUE DE PRUEBA ---
if __name__ == "__main__":
    print("Probando el Agente de Suma de forma aislada...")
    res = ejecutar_suma(10.5, 4.5)
    print(f"El resultado entregado por el agente es: {res}")