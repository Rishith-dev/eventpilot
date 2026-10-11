"""The "R" in RAG: question in, most relevant chunks out."""
from app import config
from app.rag import embedder, vectorstore


def retrieve(question: str, k: int | None = None) -> list[dict]:
    return vectorstore.search(embedder.embed_query(question), k or config.TOP_K)
