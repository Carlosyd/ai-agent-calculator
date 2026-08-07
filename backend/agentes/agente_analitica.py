# backend/agentes/agente_analitica.py
import sys
import os
import psycopg2
from psycopg2.extras import RealDictCursor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Credenciales alineadas exactamente con tu docker-compose.yml
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "agent_metrics" 
DB_USER = "admin"       
DB_PASS = "password"  # <-- Contraseña corregida      

def _conectar():
    """Función auxiliar (DRY) para no repetir el bloque de conexión."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def obtener_estadisticas() -> dict:
    """Agente especialista en consultar métricas generales de la base de datos."""
    print("📊 [Agente Analítica] Activado: Consultando métricas generales en PostgreSQL...")
    
    try:
        conexion = _conectar()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)
        
        # 1. Total de operaciones
        cursor.execute("SELECT COUNT(*) as total_operaciones FROM operaciones_agente;")
        total_ops = cursor.fetchone()['total_operaciones']
        
        # 2. Desglose de uso por cada agente
        cursor.execute("""
            SELECT nombre_agente, COUNT(*) as cantidad 
            FROM operaciones_agente 
            GROUP BY nombre_agente;
        """)
        uso_por_agente = cursor.fetchall()
        
        # 3. Total de errores
        cursor.execute("SELECT COUNT(*) as total_errores FROM operaciones_agente WHERE estado = 'error';")
        total_errores = cursor.fetchone()['total_errores']
        
        # 4. Tiempo de ejecución
        cursor.execute("SELECT AVG(tiempo_ejecucion_ms) as tiempo_promedio_ms FROM operaciones_agente;")
        tiempo_prom = cursor.fetchone()['tiempo_promedio_ms']
        
        cursor.close()
        conexion.close()
        
        print("✅ Métricas extraídas exitosamente.")
        return {
            "total_operaciones": total_ops,
            "uso_por_agente": uso_por_agente,
            "total_errores": total_errores,
            "tiempo_promedio_ms": round(tiempo_prom, 2) if tiempo_prom else 0
        }

    except Exception as e:
        mensaje_error = f"Error al conectar con la BD: {str(e)}"
        print(f"❌ {mensaje_error}")
        return {"error": mensaje_error}

def obtener_herramienta_mas_errores() -> dict:
    """Retorna el agente/herramienta que más ha fallado."""
    try:
        conexion = _conectar()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT nombre_agente as operacion, COUNT(*) as total 
            FROM operaciones_agente 
            WHERE estado = 'error' 
            GROUP BY nombre_agente 
            ORDER BY total DESC 
            LIMIT 1;
        """)
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if resultado:
            return {"operacion": resultado["operacion"], "total": resultado["total"]}
        return {"operacion": "Ninguna", "total": 0}
        
    except Exception as e:
        return {"error": str(e)}

def obtener_herramienta_mas_lenta() -> dict:
    """Retorna el agente/herramienta con el promedio de latencia más alto."""
    try:
        conexion = _conectar()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT nombre_agente as operacion, AVG(tiempo_ejecucion_ms) as promedio_ms 
            FROM operaciones_agente 
            GROUP BY nombre_agente 
            ORDER BY promedio_ms DESC 
            LIMIT 1;
        """)
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if resultado and resultado["promedio_ms"] is not None:
            return {"operacion": resultado["operacion"], "promedio_ms": round(resultado["promedio_ms"], 2)}
        return {"operacion": "Ninguna", "promedio_ms": 0}
        
    except Exception as e:
        return {"error": str(e)}

def obtener_operaciones_hoy() -> dict:
    """Cuenta cuántas operaciones se han hecho en el día actual."""
    try:
        conexion = _conectar()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)
        
        # 🛠️ FIX: Ahora sí, apuntando a la columna correcta 'fecha_registro'
        cursor.execute("""
            SELECT COUNT(*) as total_hoy 
            FROM operaciones_agente 
            WHERE DATE(fecha_registro) = CURRENT_DATE;
        """)
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        return {"total_hoy": resultado["total_hoy"] if resultado else 0}
        
    except Exception as e:
        return {"error": str(e)}

# --- BLOQUE DE PRUEBA ---
if __name__ == "__main__":
    print("Probando el Agente Analítico de forma aislada...\n")
    
    print("1. Estadísticas Generales:")
    print(obtener_estadisticas())
    
    print("\n2. Herramienta con Más Errores:")
    print(obtener_herramienta_mas_errores())
    
    print("\n3. Herramienta Más Lenta:")
    print(obtener_herramienta_mas_lenta())
    
    print("\n4. Operaciones de Hoy:")
    print(obtener_operaciones_hoy())