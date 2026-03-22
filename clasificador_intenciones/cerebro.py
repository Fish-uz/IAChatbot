# cerebro.py (Versión Chat Interactivo con Memoria y Logs)
from clasificador import clasificar_mensaje
from buscar_en_memoria import realizar_busqueda
import google.generativeai as genai
import os
import logging
from dotenv import load_dotenv

# --- CONFIGURACIÓN INICIAL ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='sistema.log',
    filemode='a'
)

# Lista para mantener la memoria de corto plazo
historial_de_mensajes = []

def responder_con_contexto(pregunta, contexto, historial):
    model = genai.GenerativeModel('models/gemini-flash-latest')
    texto_historial = "\n".join(historial[-10:]) 

    prompt = f"""
    Eres el asistente personal de Frank. Tu objetivo es ayudarlo usando su información profesional y técnica.
    
    OJO - IMPORTANTE: 
    A veces los documentos vienen con espacios entre letras (ejemplo: 'B F C' en lugar de 'BFC'). 
    Debes ser inteligente, unir las letras mentalmente y entender el cargo.
    
    HISTORIAL:
    {texto_historial}
    
    DOCUMENTOS DE FRANK (Analiza esto con cuidado):
    {contexto}
    
    PREGUNTA DEL USUARIO: {pregunta}
    
    REGLAS DE ORO:
    1. Si en el contexto aparece 'B F C' o 'Banco Fondo Comun', responde qué hizo allí (Especialista de Distribución).
    2. Si aparece 'Ubii' o 'Jata', usa esa info.
    3. Si es de Internet/Cantv, sigue los 7 pasos.
    4. Responde de forma DIRECTA y NATURAL. No digas "según el fragmento". Di: "En BFC fuiste Especialista de Distribución y te encargaste de...".
    """
    respuesta = model.generate_content(prompt)
    return respuesta.text

def iniciar_chat():
    """
    Bucle principal para chatear con el bot en la terminal.
    """
    print("============================================")
    print("   🤖 BIENVENIDO AL CHATBOT DE FRANK")
    print("   (Escribe 'salir' para finalizar)")
    print("============================================\n")

    while True:
        # 1. Pedimos la entrada del usuario
        pregunta = input("👤 Tú: ")

        # 2. Condición de salida
        if pregunta.lower() in ["salir", "exit", "quit", "finalizar"]:
            logging.info("El usuario finalizó la sesión.")
            print("🤖 Bot: ¡Hasta luego, Frank! Suerte con el código.")
            break

        # 3. Clasificamos la intención
        intencion = clasificar_mensaje(pregunta)
        
        # 4. Lógica de respuesta mejorada
        if intencion == "SOPORTE" or intencion == "VENTAS": # <--- Ahora ambos buscan
            logging.info(f"Ruta: {intencion} - Pregunta: {pregunta}")
            
            # Buscamos en la base de datos (aquí encontrará soporte o precios)
            texto_extraido = realizar_busqueda(pregunta)
            
            # Generamos respuesta con el contexto del archivo TXT
            respuesta = responder_con_contexto(pregunta, texto_extraido, historial_de_mensajes)
            print(f"🤖 Bot [{intencion.capitalize()}]: {respuesta}\n")
            
        else:
            logging.info(f"Ruta: GENERAL - Pregunta: {pregunta}")
            respuesta = "¡Hola! Soy tu asistente. ¿En qué puedo apoyarte hoy?"
            print(f"🤖 Bot [General]: {respuesta}\n")

        # 5. ACTUALIZACIÓN DE MEMORIA: Guardamos la interacción actual
        historial_de_mensajes.append(f"Usuario: {pregunta}")
        historial_de_mensajes.append(f"Bot: {respuesta}")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    iniciar_chat()