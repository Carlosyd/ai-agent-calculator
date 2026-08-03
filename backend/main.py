from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union
import ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 1. DEFINICIÓN DE HERRAMIENTAS (LAS FUNCIONES PURAS)
# ==========================================
def herramienta_suma(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Suma dos números para obtener un resultado exacto. 
    ATENCIÓN REGLA ESTRICTA: Si el usuario escribe los números con letras, 
    conviértelos a su valor numérico antes de pasarlos a los argumentos.
    """
    print(f"\n⚙️ [SISTEMA]: Ejecutando herramienta_suma -> {a} + {b}")
    return a + b

def herramienta_resta(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Resta el segundo número (b) al primer número (a). Convierte números en letras a dígitos."""
    print(f"\n⚙️ [SISTEMA]: Ejecutando herramienta_resta -> {a} - {b}")
    return a - b

def herramienta_multiplicacion(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiplica dos números para obtener el producto. Convierte números en letras a dígitos."""
    print(f"\n⚙️ [SISTEMA]: Ejecutando herramienta_multiplicacion -> {a} * {b}")
    return a * b

def herramienta_division(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Divide el primer número (a) entre el segundo (b). Convierte números en letras a dígitos."""
    print(f"\n⚙️ [SISTEMA]: Ejecutando herramienta_division -> {a} / {b}")
    return a / b

def herramienta_probabilidad_momio(momio: Union[int, float]) -> Union[int, float]:
    """
    Calcula la probabilidad implícita detectando automáticamente si el momio es Americano o Decimal.
    """
    try:
        momio = float(momio)
    except ValueError:
        raise ValueError("El agente no pudo extraer un número válido para el momio.")

    print(f"\n⚙️ [SISTEMA]: Ejecutando herramienta_probabilidad_momio -> Momio: {momio}")
    
    if momio == 0:
        return 0.0

    # AUTO-DETECCIÓN DE FORMATO
    if 1 < momio < 100:
        # Lógica para Momios Decimales (Ej. 1.5, 2.10)
        prob = 1 / momio
    elif momio <= -100:
        # Lógica para Momios Americanos Favoritos (Ej. -400)
        prob = abs(momio) / (abs(momio) + 100)
    elif momio >= 100:
        # Lógica para Momios Americanos Underdogs (Ej. +130)
        prob = 100 / (momio + 100)
    else:
        raise ValueError("Formato no reconocido. Usa Americano (-150, 130) o Decimal (1.5).")
        
    return round(prob * 100, 2)
# Catálogo maestro para el enrutador
catalogo_herramientas = {
    'herramienta_suma': herramienta_suma,
    'herramienta_resta': herramienta_resta,
    'herramienta_multiplicacion': herramienta_multiplicacion,
    'herramienta_division': herramienta_division,
    'herramienta_probabilidad_momio': herramienta_probabilidad_momio
}

# ==========================================
# 2. ESQUEMAS DE COMUNICACIÓN
# ==========================================
class MensajeUsuario(BaseModel):
    mensaje: str
    herramienta_sugerida: str | None = None

# ==========================================
# 3. EL CEREBRO DEL AGENTE (ENDPOINT)
# ==========================================
@app.post("/api/chat")
def procesar_mensaje(datos: MensajeUsuario):
    print(f"👤 React envió: {datos.mensaje} | Menú seleccionado: {datos.herramienta_sugerida}")
    
    mensajes = [{'role': 'user', 'content': datos.mensaje}]
    
    # Le damos TODAS las herramientas al LLM para que entienda bien el texto y no intente adivinar
    herramientas_activas = list(catalogo_herramientas.values())

    # Inyección dinámica del System Prompt para guiar al modelo
    if datos.herramienta_sugerida:
        nombre_tool = f"herramienta_{datos.herramienta_sugerida}"
        mensajes.insert(0, {
            'role': 'system', 
            'content': f'''CONTEXTO DE INTERFAZ: El usuario tiene seleccionada la {nombre_tool}.
            
            REGLAS DE DECISIÓN ESTRICTAS:
            1. Si el usuario escribe SOLO números separados por espacios, DEBES asumir que quiere usar la {nombre_tool} OBLIGATORIAMENTE.
            2. Si el texto pide EXPLÍCITAMENTE otra operación usando verbos, usa la herramienta que corresponda a esa palabra.
            
            Extrae los parámetros y usa la herramienta en silencio sin generar texto conversacional.'''
        })

    # La llamada a la API con TEMPERATURA 0 (Determinismo total)
    respuesta_llm = ollama.chat(
        model='llama3.1',
        messages=mensajes,
        tools=herramientas_activas,
        options={'temperature': 0.0}
    )
    
    # ==========================================
    # 4. CAPA DE VALIDACIÓN Y ENRUTADOR DINÁMICO (ROUTER)
    # ==========================================
    if respuesta_llm.message.tool_calls:
        for tool_call in respuesta_llm.message.tool_calls:
            nombre_funcion_llm = tool_call.function.name 
            
            # 1. VALIDACIÓN DE ESTADO: Comparamos el LLM con la UI de React
            nombre_funcion_ui = f"herramienta_{datos.herramienta_sugerida}" if datos.herramienta_sugerida else None
            
            if nombre_funcion_ui and nombre_funcion_llm != nombre_funcion_ui:
                nombres_bonitos = {
                    "herramienta_suma": "SUMA",
                    "herramienta_resta": "RESTA",
                    "herramienta_multiplicacion": "MULTIPLICACIÓN",
                    "herramienta_division": "DIVISIÓN",
                    "herramienta_probabilidad_momio": "PROBABILIDAD"
                }
                operacion_deseada = nombres_bonitos.get(nombre_funcion_llm, "otra operación")
                operacion_actual = nombres_bonitos.get(nombre_funcion_ui, "desconocida")
                
                return {
                    "respuesta": f"⚠️ ALERTA DE SISTEMA: El texto requiere una {operacion_deseada}, pero tienes seleccionado {operacion_actual}. Por favor, cambia de herramienta en el menú izquierdo.", 
                    "tipo": "error"
                }
            
            # 2. EJECUCIÓN DINÁMICA (Si pasó la validación)
            if nombre_funcion_llm in catalogo_herramientas:
                argumentos = tool_call.function.arguments
                funcion_a_ejecutar = catalogo_herramientas[nombre_funcion_llm]
                
                try:
                    # Desempaquetado dinámico de parámetros (el truco maestro)
                    resultado = funcion_a_ejecutar(**argumentos)
                    
                    # Interfaz de respuesta dinámica basada en la herramienta
                    if "probabilidad" in nombre_funcion_llm:
                        momio_ingresado = argumentos.get('momio')
                        return {
                            "respuesta": f"[SYS_EXEC] Análisis de momio ({momio_ingresado}): Probabilidad implícita = {resultado}%", 
                            "tipo": "info"
                        }
                    else:
                        val_a = argumentos.get('a')
                        val_b = argumentos.get('b')
                        simbolo = "+" if "suma" in nombre_funcion_llm else "-" if "resta" in nombre_funcion_llm else "*" if "multi" in nombre_funcion_llm else "/"
                        
                        return {
                            "respuesta": f"[SYS_EXEC] Operación ejecutada: {val_a} {simbolo} {val_b} = {resultado}", 
                            "tipo": "info"
                        }
                        
                except Exception as e:
                    return {
                        "respuesta": f"ERROR_EJECUCIÓN: Revisa los parámetros. Detalle: {str(e)}", 
                        "tipo": "error"
                    }
                
    # Fallback si el modelo falla o quiere conversar
    return {
        "respuesta": f"ERROR_SINTAXIS: Conflicto de parámetros o entrada no válida. Output del modelo: {respuesta_llm.message.content}", 
        "tipo": "error"
    }