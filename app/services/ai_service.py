# Folder: /app/services
"""AI service wrapper: calls to LLMs (Gemini / OpenAI) via integration clients.

This service is responsible for all AI reasoning and model orchestration. Other
services must not call LLMs directly; they should call this service instead.
"""
from typing import Any, Dict, Optional
import asyncio

from pydantic import BaseModel

from app.integrations.gemini_client import GeminiClient
from app.integrations.openai_client import OpenAIClient
from app.utils.logging import get_logger

logger = get_logger(__name__)


class AIResponse(BaseModel):
    text: str
    raw: Optional[Dict[str, Any]] = None


class AIService:
    """Service that wraps Gemini/OpenAI clients and provides a unified API.

    Methods are async to allow integration clients to run in thread-pools or
    be replaced with async clients later.
    """

    def __init__(self, gemini_api_key: Optional[str] = None, openai_api_key: Optional[str] = None) -> None:
        self.gemini = GeminiClient(gemini_api_key or "")
        self.openai = OpenAIClient(openai_api_key or "")

    async def run_json(self, prompt: str, inputs: Dict[str, Any]) -> AIResponse:
        """Run a prompt that expects structured JSON output.

        This method delegates to the OpenAI client for structured JSON parsing (if supported).
        """
        def _call():
            logger.debug("AI run_json prompt=%s inputs=%s", prompt, inputs)
            res = self.openai.generate_text(prompt + "\nInputs:" + str(inputs))
            return res

        raw = await asyncio.to_thread(_call)
        return AIResponse(text=raw.get("text", ""), raw=raw)

    async def run_vision(self, image_url: str) -> AIResponse:
        """Run vision model on an image via Gemini Client."""
        def _call():
            logger.debug("AI run_vision image_url=%s", image_url)
            return self.gemini.analyze_image(image_url.encode() if isinstance(image_url,str) else image_url)

        raw = await asyncio.to_thread(_call)
        return AIResponse(text=str(raw), raw=raw)

    async def run_video(self, video_url: str) -> AIResponse:
        """Run a video model analysis; uses Gemini/Vertex APIs to analyze a video URL."""
        def _call():
            logger.debug("AI run_video video_url=%s", video_url)
            return self.gemini.analyze_image(b"video:" + (video_url.encode() if isinstance(video_url,str) else video_url))

        raw = await asyncio.to_thread(_call)
        return AIResponse(text=str(raw), raw=raw)

    async def run_chat(self, messages: Dict[str, Any]) -> AIResponse:
        """Run a chat-style interaction via OpenAI.

        `messages` should contain role/content structured messages.
        """
        def _call():
            logger.debug("AI run_chat messages=%s", messages)
            prompt = str(messages)
            return self.openai.generate_text(prompt)

        raw = await asyncio.to_thread(_call)
        return AIResponse(text=raw.get("text", ""), raw=raw)
