# clasificador.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def clasificar_mensaje(mensaje_usuario):
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    prompt = f"""
    Eres un experto en clasificación de intenciones para un sistema de atención al cliente.
    Tu tarea es leer el MENSAJE y responder ÚNICAMENTE con una de estas tres palabras: 'SOPORTE', 'VENTAS' o 'GENERAL'.

    REGLAS DE CLASIFICACIÓN:
    1. SOPORTE: 
       - EXCLUSIVAMENTE sobre fallas de Internet ABA Cantv (módem, cables, conexión).
       - NO incluyas aquí nada sobre la carrera de Frank.

    2. VENTAS: 
       - Preguntas sobre el catálogo de equipos, precios de routers, modelos AX12, Archer, etc.
       - Si preguntan por "precio", "costo" o "comprar", es VENTAS.

    3. GENERAL: 
       - Saludos, despedidas.
       - TODO lo relacionado con Frank (BFC, Ubii, experiencia, estudios, CV).

    MENSAJE: "{mensaje_usuario}"
    RESPUESTA (SOLO LA PALABRA):"""

    try:
        respuesta = model.generate_content(prompt)
        # Limpiamos la respuesta por si Gemini añade espacios o puntos
        intencion = respuesta.text.strip().upper()
        
        # Validación de seguridad
        if intencion in ["SOPORTE", "VENTAS", "GENERAL"]:
            return intencion
        else:
            return "GENERAL" # Por defecto si algo falla
    except Exception as e:
        print(f"Error en el clasificador: {e}")
        return "GENERAL"