# Folder: /app/workflows
"""Invoice summary workflow (GPT + billing pipeline).
"""
from typing import Dict, List


WORKFLOW_NAME = "invoice_summary"
VERSION = "0.1"
DESCRIPTION = "Parse invoice, summarize line items, and optionally route to billing service."


def get_steps(context: Dict[str, object], state: Dict[str, object]) -> List[str]:
    return ["extract_invoice", "billing"]
