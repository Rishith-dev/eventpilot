"""End-to-end retrieval test WITHOUT the real embedding model.

A tiny fake embedder (hashed bag-of-words) stands in for sentence-transformers, so this
test runs in seconds, offline, and still checks: load -> chunk -> store -> search.
"""
import math
import re
import zlib

from app import config
from app.rag import chunker, loader, vectorstore

DIMS = 256


def fake_embed(texts):
    vectors = []
    for text in texts:
        vec = [0.0] * DIMS
        for word in re.findall(r"[a-z]+", text.lower()):
            vec[zlib.crc32(word.encode()) % DIMS] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        vectors.append([v / norm for v in vec])
    return vectors


def build_index():
    docs = loader.load_directory(config.RAW_DOCS_DIR)
    assert docs, "sample documents are missing from data/raw"
    chunks = []
    for doc in docs:
        chunks += chunker.chunk_document(doc.source, doc.text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    vectorstore.reset_collection()
    vectorstore.add_chunks(chunks, fake_embed([c.text for c in chunks]))
    return chunks


def test_food_question_finds_the_event_report(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CHROMA_DIR", tmp_path / "chroma")
    chunks = build_index()
    assert vectorstore.count() == len(chunks)

    # The fake embedder only matches shared words, so the query uses details that appear
    # in the report (price per plate, rice shortage, queue) and not in the checklist.
    hits = vectorstore.search(fake_embed(["lunch per plate caterer rice short queue counters"])[0], 3)
    assert hits
    assert hits[0]["source"] == "sample_past_event_report_technova_2025.md"
    assert 0 < hits[0]["score"] <= 1


def test_sponsor_tier_question_finds_the_proposal(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CHROMA_DIR", tmp_path / "chroma")
    build_index()

    hits = vectorstore.search(fake_embed(["sponsorship tiers title sponsor gold silver benefits"])[0], 3)
    assert hits[0]["source"] == "sample_sponsorship_proposal_template.md"


def test_search_on_empty_database_returns_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CHROMA_DIR", tmp_path / "empty")
    assert vectorstore.search(fake_embed(["anything"])[0], 3) == []
