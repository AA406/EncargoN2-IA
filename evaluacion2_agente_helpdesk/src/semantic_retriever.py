from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import re

import chromadb
from chromadb.utils import embedding_functions

from .config import DATA_DIR, VECTOR_DB_DIR, EMBEDDING_MODEL


@dataclass
class RetrievedDocument:
    text: str
    source: str
    score: float


class SemanticRetriever:
    """Recuperador semántico basado en ChromaDB y Sentence Transformers."""

    def __init__(self, data_dir: Path = DATA_DIR, persist_dir: Path = VECTOR_DB_DIR):
        self.data_dir = Path(data_dir)
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
        self.collection = self.client.get_or_create_collection(
            name="helpdesk_knowledge_base",
            embedding_function=self.embedding_fn,
            metadata={"description": "Base de conocimiento semántica para agente Helpdesk"},
        )

    @staticmethod
    def _split_markdown(text: str, chunk_size: int = 900, overlap: int = 120) -> List[str]:
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end >= len(text):
                break
            start = max(end - overlap, 0)
        return chunks

    def reset_index(self) -> None:
        try:
            self.client.delete_collection("helpdesk_knowledge_base")
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name="helpdesk_knowledge_base",
            embedding_function=self.embedding_fn,
            metadata={"description": "Base de conocimiento semántica para agente Helpdesk"},
        )

    def ingest(self, force: bool = False) -> int:
        if force:
            self.reset_index()

        files = sorted(self.data_dir.glob("*.md"))
        ids, docs, metadatas = [], [], []
        for file_path in files:
            content = file_path.read_text(encoding="utf-8")
            chunks = self._split_markdown(content)
            for index, chunk in enumerate(chunks):
                ids.append(f"{file_path.stem}-{index}")
                docs.append(chunk)
                metadatas.append({"source": file_path.name, "chunk": index})

        if not docs:
            return 0

        existing = set(self.collection.get().get("ids", []))
        new_ids, new_docs, new_metas = [], [], []
        for item_id, doc, meta in zip(ids, docs, metadatas):
            if item_id not in existing:
                new_ids.append(item_id)
                new_docs.append(doc)
                new_metas.append(meta)

        if new_docs:
            self.collection.add(ids=new_ids, documents=new_docs, metadatas=new_metas)
        return len(new_docs)

    def search(self, query: str, top_k: int = 4) -> List[Dict]:
        if self.collection.count() == 0:
            self.ingest(force=False)

        result = self.collection.query(query_texts=[query], n_results=top_k)
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        retrieved = []
        for doc, meta, distance in zip(documents, metadatas, distances):
            # Chroma entrega distancia. Mientras menor sea, más similar.
            score = 1 / (1 + float(distance))
            retrieved.append({
                "text": doc,
                "source": meta.get("source", "desconocido"),
                "chunk": meta.get("chunk", 0),
                "distance": round(float(distance), 4),
                "score": round(score, 3),
            })
        return retrieved
