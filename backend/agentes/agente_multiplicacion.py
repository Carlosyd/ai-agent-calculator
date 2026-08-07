# backend/agentes/agente_multiplicacion.py
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import registrar_operacion

def ejecutar_multiplicacion(num1: float, num2: float) -> float:
    print(f"✖️ [Agente Multiplicación] Activado: calculando {num1} * {num2}...")
    tiempo_inicio = time.time()
    
    try:
        resultado = num1 * num2
        estado = "exito"
        mensaje_error = None
    except Exception as e:
        resultado = None
        estado = "error"
        mensaje_error = str(e)
        
    tiempo_ms = int((time.time() - tiempo_inicio) * 1000)
    
    registrar_operacion(
        nombre_agente="agente_multiplicacion",
        peticion=f"{num1} * {num2}",
        respuesta=str(resultado),
        tiempo_ms=tiempo_ms,
        estado=estado,
        error=mensaje_error
    )
    return resultado

if __name__ == "__main__":
    res = ejecutar_multiplicacion(10.0, 4.5)
    print(f"Resultado: {res}")