# Folder: /app/actions
"""Invoice creation and billing via BillingService.
"""
from typing import Any, Dict
import asyncio

from app.services.billing_service import BillingService
from app.utils.logging import get_logger

logger = get_logger(__name__)
billing_service = BillingService()


async def handle(payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        amount = payload.get("amount")
        currency = payload.get("currency") or "usd"
        customer_id = payload.get("customer_id") or context.get("customer_id")
        if amount is None or not customer_id:
            raise ValueError("amount and customer_id are required")
        result = await asyncio.to_thread(billing_service.charge, int(amount), currency, customer_id)
        return {"status": "success", "data": {"billing": result}}
    except Exception as e:
        logger.exception("invoice_create failed: %s", e)
        return {"status": "error", "code": "INVOICE_CREATE_FAILED", "message": str(e)}
