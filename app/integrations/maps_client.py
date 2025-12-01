# Folder: /app/integrations
"""Maps client wrapper.
"""
from typing import Any, Dict


class MapsClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def geocode(self, address: str) -> Dict[str, Any]:
        return {"address": address, "lat": 0.0, "lon": 0.0}
