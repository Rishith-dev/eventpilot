"""Step 4: store vectors in ChromaDB (a local vector database) and search them.

Search = "find the chunks whose vectors are closest to the question's vector".
We use cosine distance, and report similarity = 1 - distance (higher is better).
"""
import chromadb

from app import config
from app.rag.chunker import Chunk


def _client():
    return chromadb.PersistentClient(path=str(config.CHROMA_DIR))


def _collection():
    return _client().get_or_create_collection(
        name=config.COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )


def reset_collection() -> None:
    """Delete everything so the next ingest starts clean."""
    try:
        _client().delete_collection(config.COLLECTION_NAME)
    except Exception:
        pass  # nothing to delete the first time


def add_chunks(chunks: list[Chunk], embeddings: list[list[float]]) -> None:
    _collection().upsert(
        ids=[f"{c.source}::{c.index}" for c in chunks],
        documents=[c.text for c in chunks],
        embeddings=embeddings,
        metadatas=[{"source": c.source, "chunk_index": c.index} for c in chunks],
    )


def count() -> int:
    return _collection().count()


def search(query_embedding: list[float], k: int) -> list[dict]:
    total = count()
    if total == 0:
        return []
    result = _collection().query(query_embeddings=[query_embedding], n_results=min(k, total))
    hits = []
    for text, meta, dist in zip(result["documents"][0], result["metadatas"][0], result["distances"][0]):
        hits.append(
            {
                "text": text,
                "source": meta["source"],
                "chunk_index": meta["chunk_index"],
                "score": round(1 - dist, 4),
            }
        )
    return hits
