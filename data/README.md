# Data folder

`data/raw/` is where documents for the knowledge base go. Supported types: `.txt`, `.md`, `.pdf`, `.docx`.

## What's here now

Three **synthetic** samples (`sample_*`) so the pipeline runs on day one. They are made up.

## Adding your real club documents

Good candidates: past event reports, sponsorship proposals, logistics checklists, budget sheets (as text), marketing calendars, post-event feedback summaries.

**Remove private details before you add anything:**

- names of students, faculty and sponsor contacts (use roles like `[Sponsor contact]`)
- phone numbers, email addresses, bank or payment details
- anything the club or a sponsor would not want public

## Privacy rule for GitHub

`.gitignore` is set so that **only `sample_*` files are ever committed**. Your real documents stay on your laptop. The public repo, and any live demo, uses the synthetic samples only. Check `git status` before every push.

## Rebuilding the database

After adding or changing documents, from the `backend/` folder:

```
python -m scripts.ingest --reset
```

The vector database lives in `data/chroma/` and is not committed.
