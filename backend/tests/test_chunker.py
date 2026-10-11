import pytest

from app.rag.chunker import chunk_document, split_text


def test_short_text_is_one_chunk():
    assert split_text("Hello world.", 800, 150) == ["Hello world."]


def test_empty_text_gives_no_chunks():
    assert split_text("   \n\n  ", 800, 150) == []


def test_long_text_is_split_and_bounded():
    text = "\n\n".join(f"Paragraph {i}. " + "word " * 40 for i in range(30))
    chunks = split_text(text, chunk_size=500, overlap=100)
    assert len(chunks) > 1
    assert all(len(c) <= 500 + 100 + 2 for c in chunks)


def test_one_huge_paragraph_is_hard_split():
    text = "x" * 2000
    chunks = split_text(text, chunk_size=500, overlap=100)
    assert len(chunks) > 1
    assert all(len(c) <= 500 + 100 + 2 for c in chunks)


def test_overlap_carries_context_forward():
    paragraphs = [" ".join(f"tok{i}_{j}" for j in range(30)) for i in range(6)]
    chunks = split_text("\n\n".join(paragraphs), chunk_size=400, overlap=80)
    assert len(chunks) > 1
    for before, after in zip(chunks, chunks[1:]):
        last_word = before.split()[-1]
        assert last_word in after


def test_invalid_settings_raise():
    with pytest.raises(ValueError):
        split_text("abc", chunk_size=0, overlap=0)
    with pytest.raises(ValueError):
        split_text("abc", chunk_size=100, overlap=100)


def test_chunk_document_keeps_source_and_order():
    text = "\n\n".join(f"Paragraph {i}. " + "word " * 40 for i in range(10))
    chunks = chunk_document("report.md", text, chunk_size=300, overlap=50)
    assert [c.index for c in chunks] == list(range(len(chunks)))
    assert all(c.source == "report.md" for c in chunks)
