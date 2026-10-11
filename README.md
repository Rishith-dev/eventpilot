# EventPilot

An AI copilot for student event teams. Describe an event in plain words and get a sponsor pitch, a logistics checklist, a marketing calendar and a budget breakdown, grounded in what your club has already learned from past events.

> **Status:** in development. Target completion: 24 Nov 2026. See [docs/ROADMAP.md](docs/ROADMAP.md).

## The problem

Every year a new team takes over and starts from zero. Old proposals and checklists are lost in chat groups and drive folders, and writing sponsor emails and budgets takes forever.

## How it works

1. **RAG:** club documents are split into chunks, embedded, and stored in a vector database. For every request the most relevant chunks are retrieved.
2. **LLM:** a language model writes the answer using only those retrieved chunks, and cites the documents it used.
3. **Tools:** a budget calculator, timeline generator and PDF exporter are called by the model when needed, so numbers are computed, not guessed.

Details: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## What works today

- Document loading (txt, md, pdf, docx), chunking, local embeddings, ChromaDB search
- `ingest` and `query` command-line scripts
- Health-check API endpoint
- Unit and end-to-end retrieval tests

Everything else is on the roadmap.

## Tech stack

Python, FastAPI, ChromaDB, sentence-transformers (local embeddings). LLM: Gemini or Groq free tier, with Ollama as an offline option (Phase 2).

## Quick start

Python 3.10+ (3.11 or 3.12 recommended).

```bash
# 1. create and activate a virtual environment (from the project root)
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt

# 3. copy the settings file
cp .env.example .env        # Windows: copy .env.example .env

# 4. everything below runs from the backend/ folder
cd backend
pytest                                   # run the tests
python -m scripts.ingest --reset         # build the knowledge base (first run downloads a ~90 MB model)
python -m scripts.query "What did we do for food last year?"
uvicorn app.main:app --reload            # API at http://127.0.0.1:8000/docs
```

## Project structure

```
backend/app/rag/      loader, chunker, embedder, vectorstore, retriever
backend/app/llm/      LLM providers (Phase 2)
backend/app/tools/    LLM tools (Phase 3)
backend/scripts/      ingest.py, query.py
backend/tests/        pytest tests
data/raw/             documents for the knowledge base
docs/                 architecture and roadmap
frontend/             UI (Phase 4)
```

## Privacy

Real club documents are never committed. The public repo contains synthetic samples only. See [data/README.md](data/README.md).
