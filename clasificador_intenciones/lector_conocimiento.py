# lector_conocimiento.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

def cargar_manual(ruta_pdf):
    """
    Carga un archivo PDF y lo divide en trozos para que la IA lo procese mejor.
    """
    print(f"--- Leyendo documento: {ruta_pdf} ---")
    
    # 1. Cargamos el PDF
    loader = PyPDFLoader(ruta_pdf)
    paginas = loader.load()

    # 2. Dividimos el texto en fragmentos de 1000 caracteres
    # Esto ayuda a que la IA no se pierda en textos largos
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    fragmentos = text_splitter.split_documents(paginas)

    print(f"Documento dividido en {len(fragmentos)} fragmentos.")
    return fragmentos

# --- Prueba local ---
if __name__ == "__main__":
    # Asegúrate de poner un PDF cualquiera en tu carpeta para probar
    # test = cargar_manual("mi_documento.pdf") 
    pass