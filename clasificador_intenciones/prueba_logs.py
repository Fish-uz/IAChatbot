# 1. Importamos la librería nativa de Python para registros
import logging

# 2. Configuramos cómo queremos que se guarde la información
logging.basicConfig(
    # 'level': Indica que queremos guardar TODO (desde info básica hasta errores)
    level=logging.INFO,
    
    # 'format': Aquí definimos el orden de las piezas del log:
    # %(asctime)s  -> La fecha y hora automática
    # %(levelname)s -> El nivel (INFO/ERROR)
    # %(message)s   -> El texto que nosotros escribamos
    format='%(asctime)s - %(levelname)s - %(message)s',
    
    # 'filename': El nombre del archivo donde se escribirá todo
    filename='sistema.log',
    
    # 'filemode': 'a' significa "Append" (añadir). 
    # Cada vez que corras el programa, escribirá debajo de lo anterior sin borrarlo.
    filemode='a'
)

# 3. Probamos escribir diferentes tipos de mensajes
logging.info("El sistema ha iniciado correctamente.")
logging.warning("El bot detecto que queda poca bateria en el equipo.")
logging.error("No se pudo encontrar el PDF en la carpeta seleccionada.")

print("¡Proceso terminado! Revisa el archivo 'sistema.log' en tu carpeta.")