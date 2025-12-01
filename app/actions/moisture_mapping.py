# Folder: /app/actions
"""Moisture mapping action: generate moisture insights using AIService.
"""
from typing import Any, Dict
STEP_NAME = "moisture"
import asyncio

from app.services.ai_service import AIService
from app.utils.logging import get_logger

logger = get_logger(__name__)
ai_service = AIService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        prompt = payload.get("prompt") or payload.get("moisture_prompt") or "Describe moisture pattern"
            ai_resp = await ai_service.run_chat({"messages": [{"role": "user", "content": prompt}]})
            result = ai_resp.text
        return {"status": "success", "data": {"moisture_map": result}}
    except Exception as e:
        logger.exception("moisture_mapping failed: %s", e)
        return {"status": "error", "code": "MOISTURE_MAPPING_FAILED", "message": str(e)}
