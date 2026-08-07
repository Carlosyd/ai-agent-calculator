# backend/agentes/orquestador.py
import sys
import os
import time
import ollama
import ast
from typing import Union

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 🛠️ FIX: Agregamos todas las nuevas funciones de analítica
from agentes.agente_analitica import (
    obtener_estadisticas, 
    obtener_herramienta_mas_errores, 
    obtener_herramienta_mas_lenta, 
    obtener_operaciones_hoy
)
from database import registrar_operacion

# ==========================================
# 1. DEFINICIÓN DE HERRAMIENTAS
# ==========================================
def herramienta_suma(a: Union[int, float], b: Union[int, float]) -> float:
    a, b = float(a), float(b)
    print(f"\n⚙️ [SISTEMA]: Ejecutando herramienta_suma -> {a} + {b}")
    return a + b

def herramienta_resta(a: Union[int, float], b: Union[int, float]) -> float:
    a, b = float(a), float(b)
    print(f"\n⚙️ [SISTEMA]: Ejecutando herramienta_resta -> {a} - {b}")
    return a - b

def herramienta_multiplicacion(a: Union[int, float], b: Union[int, float]) -> float:
    a, b = float(a), float(b)
    print(f"\n⚙️ [SISTEMA]: Ejecutando herramienta_multiplicacion -> {a} * {b}")
    return a * b

def herramienta_division(a: Union[int, float], b: Union[int, float]) -> float:
    a, b = float(a), float(b)
    print(f"\n⚙️ [SISTEMA]: Ejecutando herramienta_division -> {a} / {b}")
    return a / b

def herramienta_probabilidad_momio(momio: Union[int, float]) -> float:
    momio = float(momio)
    print(f"\n⚙️ [SISTEMA]: Ejecutando herramienta_probabilidad_momio -> Momio: {momio}")
    if momio == 0: return 0.0
    if 1 < momio < 100: prob = 1 / momio
    elif momio <= -100: prob = abs(momio) / (abs(momio) + 100)
    elif momio >= 100: prob = 100 / (momio + 100)
    else: raise ValueError("Momio inválido.")
    return round(prob * 100, 2)

# ==========================================
# 2. MOTOR AST (EVALUADOR DETERMINISTA Y UI LOGGER)
# ==========================================
def evaluar_y_ejecutar_ast(nodo, peticion_original, respuestas_ui, tiempo_inicio):
    """Recorre el árbol de sintaxis, ejecuta herramientas y arma la interfaz visual"""
    if isinstance(nodo, ast.BinOp):
        left = evaluar_y_ejecutar_ast(nodo.left, peticion_original, respuestas_ui, tiempo_inicio)
        right = evaluar_y_ejecutar_ast(nodo.right, peticion_original, respuestas_ui, tiempo_inicio)

        if isinstance(nodo.op, ast.Add):
            res = herramienta_suma(left, right)
            simbolo, nombre_funcion = "+", "herramienta_suma"
        elif isinstance(nodo.op, ast.Sub):
            res = herramienta_resta(left, right)
            simbolo, nombre_funcion = "-", "herramienta_resta"
        elif isinstance(nodo.op, ast.Mult):
            res = herramienta_multiplicacion(left, right)
            simbolo, nombre_funcion = "*", "herramienta_multiplicacion"
        elif isinstance(nodo.op, ast.Div):
            if right == 0:
                raise ZeroDivisionError("No se puede dividir entre cero.")
            res = herramienta_division(left, right)
            simbolo, nombre_funcion = "/", "herramienta_division"

        latencia = int((time.time() - tiempo_inicio) * 1000)
        registrar_operacion(nombre_funcion, peticion_original, str(res), latencia, "exito")

        paso_num = len(respuestas_ui) + 1
        respuestas_ui.append(f"  Paso {paso_num}: {left} {simbolo} {right} = {res}")
        return res

    elif isinstance(nodo, ast.Constant):
        return float(nodo.value)
        
    elif isinstance(nodo, ast.UnaryOp):
        operando = evaluar_y_ejecutar_ast(nodo.operand, peticion_original, respuestas_ui, tiempo_inicio)
        if isinstance(nodo.op, ast.USub):
            return -operando
        elif isinstance(nodo.op, ast.UAdd):
            return operando
            
    else:
        raise ValueError("Operación no soportada en el árbol de sintaxis.")

# ==========================================
# 3. ENRUTADOR Y CEREBRO LLM (PARSER)
# ==========================================
def clasificar_intencion(peticion: str) -> str:
    """Clasificador expandido para detectar métricas específicas de base de datos."""
    peticion = peticion.lower()
    
    # 1. Intenciones específicas de analítica profunda
    if any(p in peticion for p in ["hoy", "este día", "este dia", "diarias"]):
        return "analitica_hoy"
    if any(p in peticion for p in ["errores", "falla", "equivocan", "fallan", "peor"]):
        return "analitica_errores"
    if any(p in peticion for p in ["latencia", "tarda", "lenta", "lento", "demora"]):
        return "analitica_latencia"
        
    # 2. Intención analítica general (Fallback)
    palabras_analiticas = ["estadística", "estadistica", "reporte", "historial", "métricas", "metricas", "cuántas", "cuantos"]
    if any(p in peticion for p in palabras_analiticas):
        return "analitica_general"
        
    # 3. Si no es analítica, es matemática
    return "matematica"

def procesar_peticion(peticion_usuario: str):
    intencion = clasificar_intencion(peticion_usuario)
    
    # --- FLUJOS DE ANALÍTICA ---
    if intencion == "analitica_general":
        resultados = obtener_estadisticas()
        if "error" in resultados: return f"ERROR_EJECUCIÓN: {resultados['error']}"
        return (f"📊 Reporte General:\n- Operaciones: {resultados['total_operaciones']}\n"
                f"- Errores: {resultados['total_errores']}\n"
                f"- Latencia Promedio: {resultados['tiempo_promedio_ms']} ms")
                
    elif intencion == "analitica_errores":
        res = obtener_herramienta_mas_errores() 
        if "error" in res: return f"ERROR_EJECUCIÓN: {res['error']}"
        return f"🚨 Alerta de Rendimiento:\nLa herramienta que más falla es **{res['operacion']}** con un total de {res['total']} errores registrados."
        
    elif intencion == "analitica_latencia":
        res = obtener_herramienta_mas_lenta()
        if "error" in res: return f"ERROR_EJECUCIÓN: {res['error']}"
        return f"\nLa herramienta más lenta es **{res['operacion']}**, tardando en promedio {res['promedio_ms']} ms en responder."
        
    elif intencion == "analitica_hoy":
        res = obtener_operaciones_hoy()
        if "error" in res: return f"ERROR_EJECUCIÓN: {res['error']}"
        return f"📅 Actividad del Día:\nEl sistema ha procesado **{res['total_hoy']}** operaciones el día de hoy."
        
    # --- FLUJO MATEMÁTICO (AST) ---
    elif intencion == "matematica":
        mensajes = [
            {'role': 'system', 'content': (
                'Eres un parser matemático. Tu ÚNICO trabajo es traducir texto a fórmulas puras o comandos específicos.\n'
                'REGLAS:\n'
                '1. Si es matemática, traduce a símbolos (+, -, *, /). Ejemplo: "8 mas 6 entre 2" -> "8 + 6 / 2"\n'
                '2. Soporta números negativos. Ejemplo: "menos 10 mas 5" -> "-10 + 5"\n'
                '3. Si es análisis de momios, escribe MOMIO seguido del número. Ejemplo: "probabilidad del momio -150" -> "MOMIO -150"\n'
                '4. Responde ÚNICAMENTE con la fórmula o el comando MOMIO, sin ninguna otra palabra, sin explicaciones y sin comillas.'
            )},
            {'role': 'user', 'content': peticion_usuario}
        ]
        
        tiempo_inicio = time.time()
        
        respuesta_llm = ollama.chat(
            model='llama3.1',
            messages=mensajes,
            options={'temperature': 0.0}
        )
        
        output_limpio = respuesta_llm.message.content.strip()
        respuestas_ui = []
        
        try:
            if output_limpio.upper().startswith("MOMIO"):
                valor_momio = float(output_limpio.split()[1])
                resultado = herramienta_probabilidad_momio(valor_momio)
                latencia = int((time.time() - tiempo_inicio) * 1000)
                registrar_operacion("herramienta_probabilidad_momio", peticion_usuario, str(resultado), latencia, "exito")
                return f"  Análisis de momio ({valor_momio}) = {resultado}%\n  Resultado Final: {resultado}%"
            
            else:
                arbol_sintaxis = ast.parse(output_limpio, mode='eval')
                resultado_final = evaluar_y_ejecutar_ast(arbol_sintaxis.body, peticion_usuario, respuestas_ui, tiempo_inicio)
                
                respuestas_ui.append(f"  Resultado Final: {resultado_final}")
                return "\n".join(respuestas_ui)
                
        except ZeroDivisionError as e:
            return f"ERROR MATEMÁTICO: {str(e)}"
            
        except Exception as e:
            return f"ERROR_SINTAXIS: El modelo falló al parsear. Output bruto: {output_limpio}. Detalle: {str(e)}"