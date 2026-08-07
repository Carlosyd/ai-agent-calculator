# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importamos tu orquestador maestro
from agentes.orquestador import procesar_peticion

# Inicializamos la API
app = FastAPI(title="API Calculadora Multi-Agente AI")

# Configuramos CORS (Crucial para que React no sea bloqueado por seguridad del navegador)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción aquí iría la URL de tu React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definimos el esquema de datos que esperamos recibir de React
class PeticionUsuario(BaseModel):
    mensaje: str
    
# Creamos el Endpoint
@app.post("/api/chat")
def chat_endpoint(datos: PeticionUsuario):
    print(f"\n🌐 [API] Solicitud recibida desde el Frontend: '{datos.mensaje}'")
    
    try:
        # Le pasamos el mensaje a tu orquestador y esperamos la respuesta
        resultado = procesar_peticion(datos.mensaje)
        
        # Le respondemos a React en formato JSON
        return {
            "status": "success",
            "respuesta": resultado
        }
    except Exception as e:
        print(f"❌ [API] Error interno: {e}")
        return {
            "status": "error",
            "respuesta": f"Hubo un error en el servidor: {str(e)}"
        }

# Ruta de prueba para verificar que el servidor está vivo
@app.get("/")
def health_check():
    return {"status": "ok", "mensaje": "El backend de IA está corriendo perfectamente"}