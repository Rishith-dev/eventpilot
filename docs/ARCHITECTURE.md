# EventPilot architecture

## Big picture

```
SETUP (run once, and again when documents change)
Club documents (txt / md / pdf / docx)
   -> loader        reads them into text
   -> chunker       cuts text into overlapping chunks
   -> embedder      turns each chunk into a vector
   -> vector DB     stores chunks + vectors (ChromaDB)

EVERY REQUEST
User: "Tech fest, 500 people, Rs 2L budget"
   -> embedder           turns the request into a vector
   -> vector DB          returns the closest chunks             <- "R" in RAG
   -> prompt             instructions + request + chunks
   -> LLM                writes the answer, citing sources      <- "G" in RAG
   -> tools (optional)   budget calculator, timeline, PDF export  <- agent step
   -> API response -> frontend
```

## Who does what

| Part | Job | Status |
|---|---|---|
| `app/rag/loader.py` | Read raw files into text | done (Phase 1) |
| `app/rag/chunker.py` | Split text into overlapping chunks | done (Phase 1) |
| `app/rag/embedder.py` | Local embedding model (CPU) | done (Phase 1) |
| `app/rag/vectorstore.py` | ChromaDB wrapper: store and search | done (Phase 1) |
| `app/rag/retriever.py` | Question in, relevant chunks out | done (Phase 1) |
| `app/llm/` | Provider-agnostic LLM interface (Gemini / Groq / Ollama) | Phase 2 |
| `app/tools/` | Budget calculator, timeline generator, PDF export | Phase 3 |
| `app/main.py` | FastAPI endpoints | health check only so far |
| `frontend/` | Event form, chat, results page | Phase 4 |
| evaluation | Test questions that measure answer quality | Phase 5 |

## Design decisions

- **Embeddings and vector DB run locally.** They are light, free, and work without a GPU.
- **The LLM sits behind one interface.** The main provider is a free-tier cloud API; the same code can point at a local Ollama model for an offline mode.
- **No heavy RAG framework at first.** Each step is written by hand so every line can be explained in an interview.
- **Real documents never leave the laptop.** Only synthetic samples are in the public repo.
