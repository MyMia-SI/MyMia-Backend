# Folder: /app/integrations
"""Gemini / Vertex AI client wrapper.
"""
from typing import Any, Dict


class GeminiClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        return {"analysis": "not implemented"}
