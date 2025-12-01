# Folder: /app/actions
"""AI mold analysis action: analyze image data using AIService.
"""
from typing import Any, Dict
STEP_NAME = "vision"
import asyncio

from app.services.ai_service import AIService
from app.utils.logging import get_logger

logger = get_logger(__name__)
ai_service = AIService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        image_url = payload.get("image_url") or payload.get("image")
        if image_url:
            ai_result = await ai_service.run_vision(image_url)
            result = ai_result.text
        else:
            prompt = payload.get("prompt") or payload.get("image_prompt") or "Analyze image for mold"
            ai_resp = await ai_service.run_chat({"messages": [{"role": "user", "content": prompt}]})
            result = ai_resp.text
        return {"status": "success", "data": {"analysis": result}}
    except Exception as e:
        logger.exception("ai_mold_analysis failed: %s", e)
        return {"status": "error", "code": "AI_MOLD_ANALYSIS_FAILED", "message": str(e)}
