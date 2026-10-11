"""Step 3: turn text into vectors (lists of numbers) using a small local model.

Texts with similar MEANING get vectors that point in similar directions, so we can
search by meaning instead of exact keywords. This runs on CPU - no GPU needed.
The model (~90 MB) is downloaded once, the first time you run it.
"""
from functools import lru_cache

from app import config


@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(config.EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> list[list[float]]:
    vectors = _model().encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
