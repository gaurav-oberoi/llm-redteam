"""The target under test: a local model wrapped so each attack is sent with the
guarded system prompt. Returns a model_fn the runner can call."""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Callable

from .attacks import SYSTEM_PROMPT


def ollama_target(model: str | None = None, base_url: str | None = None) -> Callable[[str], str]:
    model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def model_fn(user_prompt: str) -> str:
        payload = json.dumps({
            "model": model,
            "stream": False,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        }).encode()
        req = urllib.request.Request(f"{base_url}/api/chat", data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        return data.get("message", {}).get("content", "")

    return model_fn
