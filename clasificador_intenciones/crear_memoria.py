# Importamos las librerías necesarias
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader # Lector de PDF y Texto
from langchain_text_splitters import CharacterTextSplitter # Divisor de texto
from langchain_community.vectorstores import Chroma # Base de datos vectorial
from langchain_huggingface import HuggingFaceEmbeddings # Traductor a números (Vectores)

# --- CONFIGURACIÓN ---
# Carpeta donde vas a meter todos tus PDFs (Créalara en tu proyecto si no existe)
CARPETA_PDFS = "mis_documentos"
# Carpeta donde se guardará la memoria del bot
CARPETA_DB = "db_conocimiento"

def crear_base_datos_acumulativa():
    # 1. Verificamos si la carpeta de PDFs existe, si no, avisamos
    if not os.path.exists(CARPETA_PDFS):
        print(f"Error: La carpeta '{CARPETA_PDFS}' no existe. Créala y pon tus PDFs dentro.")
        return

    # 2. Lista para guardar todos los pedacitos de texto de todos los archivos
    fragmentos_totales = []

    # 3. Recorremos cada archivo dentro de la carpeta
    for archivo in os.listdir(CARPETA_PDFS):
        ruta_completa = os.path.join(CARPETA_PDFS, archivo)
        paginas = None

        try:
            if archivo.endswith(".pdf"):
                print(f"-> Procesando: {archivo}...")
                # Cargamos el PDF existente
                loader = PyPDFLoader(ruta_completa)
                paginas = loader.load()

            elif archivo.endswith(".txt"):
                print(f"-> Procesando TXT: {archivo}...")
                # Cargamos el TXT existente
                loader = TextLoader(ruta_completa, encoding='latin-1')
                paginas = loader.load()
        
            if paginas:
                # Lo dividimos en trozos de 1000 caracteres
                divisor = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                pedazos = divisor.split_documents(paginas)
                fragmentos_totales.extend(pedazos)

        except Exception as e:
            print(f"Error procesando {archivo}: {e}")

    if not fragmentos_totales:
        print("No se encontraron PDFs válidos para procesar.")
        return

    print(f"Total de fragmentos generados: {len(fragmentos_totales)}")

    # 4. Cargamos el modelo traductor (Aquí es donde descarga la primera vez)
    print("Cargando modelo de inteligencia artificial (Embeddings)...")
    modelo_ia = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 5. Guardamos todo en la base de datos Chroma
    # Esto sobreescribe la carpeta 'db_conocimiento' con el conocimiento de TODOS los PDFs en la carpeta
    print("Guardando en la base de datos vectorial...")
    vector_db = Chroma.from_documents(
        documents=fragmentos_totales,
        embedding=modelo_ia,
        persist_directory=CARPETA_DB
    )
    
    print("¡LISTO! Tu bot ahora conoce todo lo que hay en la carpeta 'mis_documentos'.")

# Ejecutamos el proceso
if __name__ == "__main__":
    crear_base_datos_acumulativa()