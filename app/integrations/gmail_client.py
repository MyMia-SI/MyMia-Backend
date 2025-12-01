# Folder: /app/integrations
"""Gmail API wrapper for email-related features.
"""
from typing import Any, Dict


class GmailClient:
    def __init__(self, creds: Dict[str, Any]) -> None:
        self.creds = creds

    def list_messages(self, query: str) -> Dict[str, Any]:
        return {"messages": []}
