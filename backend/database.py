import psycopg2

# Credenciales de tu contenedor Docker
DB_CONFIG = {
    "dbname": "agent_metrics",
    "user": "admin",
    "password": "password", # Confirma que esta sea tu contraseña del docker-compose
    "host": "localhost",
    "port": "5432"
}

def registrar_operacion(nombre_agente: str, peticion: str, respuesta: str, tiempo_ms: int, estado: str, error: str = None):
    """Guarda las métricas de cada agente en PostgreSQL"""
    conexion = None
    cursor = None
    try:
        conexion = psycopg2.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        
        query = """
            INSERT INTO operaciones_agente 
            (nombre_agente, peticion_usuario, respuesta_agente, tiempo_ejecucion_ms, estado, mensaje_error)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (nombre_agente, peticion, respuesta, tiempo_ms, estado, error)
        
        cursor.execute(query, valores)
        conexion.commit()
        print("✅ Operación registrada exitosamente en la base de datos.")
        
    except Exception as e:
        print(f"❌ Error al guardar métricas en BD: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

# --- BLOQUE DE PRUEBA ---
if __name__ == "__main__":
    print("Probando conexión a PostgreSQL...")
    registrar_operacion(
        nombre_agente="orquestador_test",
        peticion="prueba de conexión",
        respuesta="conexión exitosa desde python",
        tiempo_ms=150,
        estado="exito"
    )