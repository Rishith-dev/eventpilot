"""EventPilot API. Run from the backend/ folder:  uvicorn app.main:app --reload"""
from fastapi import FastAPI

app = FastAPI(title="EventPilot API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
