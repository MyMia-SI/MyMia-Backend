# Folder: /app/actions
"""Email summary generation and optional sending.
"""
from typing import Any, Dict
import asyncio

from app.services.ai_service import AIService
from app.services.email_service import EmailService
from app.utils.logging import get_logger

logger = get_logger(__name__)

ai_service = AIService()
email_service = EmailService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        emails = payload.get("emails")
        if not emails:
            raise ValueError("emails payload required")
        prompt = f"Summarize the following emails: {emails}"
        ai_resp = await ai_service.run_chat({"messages": [{"role": "user", "content": prompt}]})
        summary = ai_resp.text
        if payload.get("send_to"):
            await asyncio.to_thread(email_service.send, payload.get("send_to"), "Email Summary", str(summary))
        return {"status": "success", "data": {"summary": summary}}
    except Exception as e:
        logger.exception("email_summary failed: %s", e)
        return {"status": "error", "code": "EMAIL_SUMMARY_FAILED", "message": str(e)}
