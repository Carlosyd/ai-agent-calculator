# Calculadora Inteligente con Agentes de IA

Este proyecto es una calculadora avanzada que usa Inteligencia Artificial (Llama 3.1) para entender lo que pide el usuario y ejecutar operaciones matemáticas reales. Además de matemáticas básicas, incluye una herramienta para calcular probabilidades en apuestas deportivas. 

## ¿Cómo está construido?

El proyecto está dividido en dos partes que se comunican entre sí:

### 1. Backend
Es el motor del proyecto. Aquí hacemos lo siguiente:
* Nos conectamos con la IA local (Ollama).
* Tenemos las "herramientas" reales (Suma, Resta, Multiplicación, División y Probabilidad de Momios).
* Validamos que la IA no se equivoque. Si el usuario pide una suma, el sistema obliga a la IA a usar la herramienta de suma y calcula el resultado exacto.

### 2. Frontend 
Es la pantalla interactiva con la que interactúa el usuario. 
* Tiene un menú para elegir qué herramienta usar.
* Un chat para escribirle a la IA.
* Un diseño moderno hecho con Tailwind CSS.

## 🚀 Requisitos para usarlo

Para correr este proyecto en tu computadora necesitas tener instalado:
* [Node.js](https://nodejs.org/) (Para la interfaz gráfica)
* [Python](https://www.python.org/) (Para el servidor)
* [Ollama](https://ollama.com/) (Para correr el modelo de IA `llama3.1` de forma local)

## ⚙️ ¿Cómo levantar el proyecto?

### 1. Iniciar el Backend (Servidor)
Abre una terminal, entra a la carpeta `backend` y ejecuta:
```bash
pip install fastapi uvicorn pydantic ollama
uvicorn main:app --reload

(El servidor correrá en http://localhost:8000)

2. Iniciar el Frontend (Interfaz)
Abre otra terminal, entra a la carpeta frontend y ejecuta:

Bash
npm install
npm run dev
(La aplicación se abrirá en http://localhost:5173)

Autor: Carlos Yañez Díaz