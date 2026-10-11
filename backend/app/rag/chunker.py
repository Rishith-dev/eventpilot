"""Step 2 of RAG ingestion: split long text into overlapping chunks.

Why chunk? An embedding represents ONE idea well. A whole 10-page report squeezed
into one vector is blurry, so we cut documents into small pieces and embed each piece.
Why overlap? So a sentence cut at a chunk edge still appears whole in the next chunk.

Rules of this chunker:
- prefers to break at paragraph boundaries (blank lines)
- paragraphs longer than `chunk_size` are hard-cut (simple on purpose; improve in Week 2 if needed)
- every chunk is at most chunk_size + overlap + 2 characters long
"""
from dataclasses import dataclass


@dataclass
class Chunk:
    source: str  # which document it came from (used for citations)
    index: int   # position inside that document
    text: str


def split_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    paragraphs = [p.strip() for p in text.replace("\r\n", "\n").split("\n\n") if p.strip()]

    # 1) break up paragraphs that are too long on their own
    pieces: list[str] = []
    for para in paragraphs:
        if len(para) <= chunk_size:
            pieces.append(para)
        else:
            step = chunk_size - overlap
            for start in range(0, len(para), step):
                pieces.append(para[start:start + chunk_size])

    # 2) pack pieces together until a chunk is full, carrying a small tail forward
    chunks: list[str] = []
    current = ""
    for piece in pieces:
        if not current:
            current = piece
        elif len(current) + 2 + len(piece) <= chunk_size:
            current = f"{current}\n\n{piece}"
        else:
            chunks.append(current)
            tail = current[-overlap:] if overlap else ""
            if " " in tail:  # start the overlap at a word boundary, not mid-word
                tail = tail[tail.find(" ") + 1:]
            current = f"{tail}\n\n{piece}" if tail else piece
    if current:
        chunks.append(current)
    return chunks


def chunk_document(source: str, text: str, chunk_size: int = 800, overlap: int = 150) -> list[Chunk]:
    return [Chunk(source=source, index=i, text=t) for i, t in enumerate(split_text(text, chunk_size, overlap))]
