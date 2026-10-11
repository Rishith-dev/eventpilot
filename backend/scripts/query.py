"""Try retrieval from the terminal (no LLM yet).

Run from the backend/ folder:
    python -m scripts.query "What did we do for food last year?"
"""
import sys

from app.rag import retriever


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python -m scripts.query "your question"')
        return
    question = " ".join(sys.argv[1:])
    hits = retriever.retrieve(question)
    if not hits:
        print("Nothing found. Did you run `python -m scripts.ingest --reset` first?")
        return
    for rank, hit in enumerate(hits, start=1):
        print(f"\n[{rank}] {hit['source']}  (chunk {hit['chunk_index']}, similarity {hit['score']})")
        print(hit["text"][:400])


if __name__ == "__main__":
    main()
