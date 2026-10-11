# EventPilot roadmap

**Deadline: 24 Nov 2026.** Restarted on 11 Oct 2026, so there are 6 weeks and 2 days left.
Rule: always have something working to show. If we fall behind, we cut extras, never quality.

## Phases

| Phase | Dates | Goal | Done when |
|---|---|---|---|
| 1. Foundations | 11-18 Oct | Setup, club documents collected, ingestion and retrieval working | `query.py` finds the right chunk for most test questions |
| 2. RAG + LLM | 19-25 Oct | LLM answers with citations, FastAPI endpoints for Q&A and proposal drafts | Ask a question through the API and get a cited answer |
| 3. Tools + agent | 26 Oct-1 Nov | Budget calculator, timeline generator, PDF export; the LLM decides when to use them. Deploy a bare "hello" version | **MVP checkpoint (1 Nov):** whole flow works end to end |
| 4. Frontend | 2-8 Nov | Clean UI: event form, chat, results page | Someone else can use it without help |
| 5. Quality | 9-15 Nov | Evaluation, tests, prompt-injection guard, polish. **Feature freeze 15 Nov** | You have real accuracy numbers for the README |
| 6. Ship | 16-22 Nov | Final deploy, README, architecture diagram, demo video, portfolio page | The live link works on a phone |
| Buffer | 23-24 Nov | Fix surprises, LinkedIn post | |

---

## Phase 1 checklist (11-18 Oct)

**Sun 11 Oct - setup**
- [ ] Install Python 3.11 or 3.12, Git and VS Code
- [ ] Create a public GitHub repo called `eventpilot`
- [ ] Unzip this project, create a virtual environment, run `pip install -r requirements.txt`
- [ ] Run `pytest` inside `backend/` (all tests should pass)
- [ ] First commit and push

**Mon 12 - Tue 13 Oct - see RAG work**
- [ ] From `backend/`: `python -m scripts.ingest --reset` (first run downloads the model)
- [ ] Try `python -m scripts.query "What did we do for food last year?"` and 4-5 more questions
- [ ] Read each file in `app/rag/` and write 3 lines per file in `docs/LEARNING_NOTES.md`, in your own words

**Wed 14 - Thu 15 Oct - your real data**
- [ ] Collect 10-15 real club documents and remove private details (see `data/README.md`)
- [ ] Put them in `data/raw/` and re-run ingest with `--reset`
- [ ] Write 15 test questions in `docs/eval_questions.md`, each with the document that should answer it (this becomes your evaluation set later)

**Fri 16 - Sat 17 Oct - tune and prepare the LLM**
- [ ] Change `CHUNK_SIZE` and `CHUNK_OVERLAP` in `.env`; re-ingest and note which setting finds the right chunk more often
- [ ] Create a Gemini or Groq API key, put it in `.env`, and make one "hello" call from a small script
- [ ] Decide which provider you will use

**Sun 18 Oct - Phase 1 demo to yourself**
- [ ] `query.py` returns the right source for at least 10 of your 15 questions
- [ ] Commit, push, and write 5 lines in the README about what you learned

## Later phases (details get added as we reach them)

- [ ] **Phase 2:** LLM interface, prompt that uses retrieved chunks, citations, `/ask` and `/generate-proposal` endpoints
- [ ] **Phase 3:** budget calculator, timeline generator, PDF export, tool-calling loop, first deploy
- [ ] **Phase 4:** frontend pages and styling
- [ ] **Phase 5:** evaluation script with numbers, unit tests, guard against prompt injection, error handling
- [ ] **Phase 6:** Docker, final deploy, README with diagram, 2-minute demo video, portfolio page
