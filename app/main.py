"""FastAPI service: run the red-team suite against the configured target model."""

from __future__ import annotations

from fastapi import FastAPI

from .runner import run
from .target import ollama_target

app = FastAPI(
    title="llm-redteam",
    description="Canary-based jailbreak red-team harness for testing LLM instruction adherence.",
    version="1.0.0",
)


@app.post("/api/redteam")
def redteam() -> dict:
    return run(ollama_target()).as_dict()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}
