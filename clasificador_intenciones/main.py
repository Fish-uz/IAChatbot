# Importamos FastAPI y el esquema de datos
from fastapi import FastAPI
from pydantic import BaseModel
from clasificador import clasificar_mensaje # Importamos tu lógica de IA

# Creamos la aplicación
app = FastAPI(title="Servidor de Clasificación IA")

# Definimos qué datos debe enviarnos el cliente (un objeto con un campo 'texto')
class SolicitudMensaje(BaseModel):
    texto: str

@app.get("/")
def inicio():
    return {"mensaje": "El servidor de IA está encendido y listo."}

@app.post("/clasificar")
async def endpoint_ia(datos: SolicitudMensaje):
    """
    Recibe un JSON con texto y devuelve la clasificación.
    """
    # Llamamos a la función de Gemini
    resultado = clasificar_mensaje(datos.texto)
    
    # Respondemos al cliente
    return {
        "status": "success",
        "clasificacion": resultado,
        "texto_analizado": datos.texto
    }

# Para correr este archivo usa: uvicorn main:app --reload