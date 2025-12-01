# Folder: /app/utils
"""Error handling utilities and custom exceptions."""
from typing import Any


class OrchestratorError(Exception):
    """Base error for orchestrator-related exceptions."""


class IntegrationError(OrchestratorError):
    pass
