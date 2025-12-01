# Folder: /app/integrations
"""OpenAI / GPT client wrapper.
"""
from typing import Any, Dict


class OpenAIClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def generate_text(self, prompt: str) -> Dict[str, Any]:
        return {"text": "not implemented"}
