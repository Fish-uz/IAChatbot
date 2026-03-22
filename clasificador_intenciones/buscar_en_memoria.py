from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CARPETA_DB = "db_conocimiento"

def realizar_busqueda(pregunta_usuario):
    # 1. Cargamos el modelo de Embeddings
    modelo_ia = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 2. Abrimos la base de datos
    vector_db = Chroma(
        persist_directory=CARPETA_DB, 
        embedding_function=modelo_ia
    )

    # 3. Realizamos la búsqueda con puntaje de relevancia
    # Traemos los 2 mejores, pero los filtraremos manualmente por score
    print(f"\nBuscando información para: {pregunta_usuario}...")
    resultados_con_score = vector_db.similarity_search_with_relevance_scores(pregunta_usuario, k=2)

    # 4. Lógica para filtrar el de mayor puntaje
    contexto_final = ""
    umbral_minimo = 0.3  # Ajusta este valor (0.0 a 1.0) según necesites

    if resultados_con_score:
        # El primer resultado [0] es siempre el de mayor puntaje según Chroma
        mejor_doc, score = resultados_con_score[0]
        
        print(f"\n--- ANÁLISIS DE RELEVANCIA ---")
        print(f"Mejor coincidencia encontrada con puntaje: {score:.4f}")

        if score >= umbral_minimo:
            print(f"¡Éxito! El puntaje supera el umbral de {umbral_minimo}")
            contexto_final = mejor_doc.page_content
        else:
            print(f"Aviso: El resultado más cercano es muy débil ({score:.4f}). Se ignorará.")
            contexto_final = "No se encontró información suficientemente relevante en los documentos."
    else:
        print("No se encontraron resultados en la base de datos.")
        contexto_final = ""

    return contexto_final

# --- PRUEBA LOCAL ---
if __name__ == "__main__":
    pregunta = "Que hice en BFC?"
    resultado = realizar_busqueda(pregunta)
    print("\n--- RESULTADO FINAL PARA EL CEREBRO ---")
    print(resultado)