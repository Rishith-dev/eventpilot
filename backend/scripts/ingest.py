"""Read documents from data/raw, chunk them, embed them, and store them in the vector DB.

Run from the backend/ folder:
    python -m scripts.ingest --reset
"""
import argparse

from app import config
from app.rag import chunker, embedder, loader, vectorstore


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest club documents into the vector database")
    parser.add_argument("--reset", action="store_true", help="wipe the vector DB before ingesting")
    args = parser.parse_args()

    docs = loader.load_directory(config.RAW_DOCS_DIR)
    if not docs:
        print(f"No documents found in {config.RAW_DOCS_DIR}. Add .txt/.md/.pdf/.docx files first.")
        return

    if args.reset:
        vectorstore.reset_collection()

    all_chunks = []
    for doc in docs:
        chunks = chunker.chunk_document(doc.source, doc.text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
        print(f"{doc.source}: {len(chunks)} chunks")
        all_chunks.extend(chunks)

    print("Embedding chunks (the first run downloads the model, so it needs internet)...")
    vectors = embedder.embed_texts([c.text for c in all_chunks])
    vectorstore.add_chunks(all_chunks, vectors)
    print(f"Done. {vectorstore.count()} chunks are now in the database.")


if __name__ == "__main__":
    main()
