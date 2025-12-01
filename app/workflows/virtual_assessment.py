# Folder: /app/workflows
"""Virtual assessment workflow definition.

Video-based property assessments using video frame extraction and vision models.
"""
from typing import Dict, List


WORKFLOW_NAME = "virtual_assessment"
VERSION = "0.1"
DESCRIPTION = "Video -> Vision -> Protocol: Extract frames from video and score/produce a summary."


def get_steps(context: Dict[str, object], state: Dict[str, object]) -> List[str]:
    """Steps for virtual assessment."""
    return ["vision", "protocol"]
