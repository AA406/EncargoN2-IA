from src.semantic_retriever import SemanticRetriever


if __name__ == "__main__":
    retriever = SemanticRetriever()
    added = retriever.ingest(force=True)
    print(f"Índice semántico creado correctamente. Chunks agregados: {added}")
