# Folder: /app/utils
"""Environment & configuration helpers.

Use pydantic or any preferred configuration library to bind environment variables.
"""
from typing import Optional


class Settings:
    def __init__(self, google_project_id: Optional[str] = None) -> None:
        self.google_project_id = google_project_id


def load_settings() -> Settings:
    # Placeholder - later replace this with real environment loading.
    return Settings()
