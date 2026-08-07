# Calculadora Inteligente con Agentes de IA 

Este proyecto es una calculadora avanzada que usa Inteligencia Artificial (Llama 3.1) para entender lo que pide el usuario y ejecutar operaciones matemáticas reales. Además de matemáticas básicas incluye un sistema para consultar las estadísticas de uso en tiempo real.

## ¿Cómo está construido?

El proyecto está dividido en tres partes principales que se comunican entre sí:

### 1. Backend 
Es el motor del proyecto. Aquí hacemos lo siguiente:
* Nos conectamos con la IA local (Ollama). Ahora la IA funciona **solo como un traductor** de texto a fórmulas puras para evitar que alucine resultados.
* Un **motor matemático interno (AST)** toma la fórmula de la IA y la resuelve paso a paso. Esto garantiza resultados perfectos, respetando la jerarquía de operaciones y soportando números negativos o divisiones entre cero.
* Tenemos un "ruteador" inteligente: detecta si el usuario quiere hacer una operación matemática o si está pidiendo un reporte de estadísticas, y lo manda al agente correcto.

### 2. Base de Datos
* Usamos PostgreSQL para guardar un historial de todas las operaciones que hace el sistema.
* Registra qué herramienta se usó, cuánto tiempo tardó en responder y si hubo algún error.
* Le puedes preguntar al chat cosas como: *"¿Cuántas operaciones van hoy?"*, *"¿Qué herramienta es más lenta?"* o *"Muestra las estadísticas"*, y consultará esta base de datos.

### 3. Frontend
Es la pantalla interactiva con la que interactúa el usuario. 
* Un chat estilo terminal futireista.
* Muestra el paso a paso de cómo el sistema resolvió tu operación matemática de forma muy limpia.
* Tiene animaciones de carga y hace auto-scroll automático cuando llegan mensajes nuevos.

## 🚀 Requisitos para usarlo

Para correr este proyecto en tu computadora necesitas tener instalado:
* [Node.js](https://nodejs.org/) (Para la interfaz gráfica)
* [Python](https://www.python.org/) (Para el servidor)
* [Ollama](https://ollama.com/) (Para correr el modelo de IA `llama3.1` de forma local)
* [Docker](https://www.docker.com/) (Para levantar la base de datos PostgreSQL)

## ⚙️ ¿Cómo levantar el proyecto?

### 1. Iniciar la Base de Datos
Abre una terminal en la raíz del proyecto y levanta el contenedor:
```bash
docker-compose up -d

2. Iniciar el Backend (Servidor)
Abre una terminal, entra a la carpeta backend y ejecuta:

Bash
pip install fastapi uvicorn pydantic ollama psycopg2
uvicorn main:app --reload
(El servidor correrá en http://localhost:8000)

3. Iniciar el Frontend (Interfaz)
Abre otra terminal, entra a la carpeta frontend y ejecuta:

Bash
npm install
npm run dev
(La aplicación se abrirá en http://localhost:5173)

Autor: Carlos Yañez Díaz