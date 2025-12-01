# Folder: /app/workflows
"""Job classifier workflow definition (classifies job type)."""
from typing import Dict, List


WORKFLOW_NAME = "job_classifier"
VERSION = "0.1"
DESCRIPTION = "Classify a job into one of several categories based on metadata and media."


def get_steps(context: Dict[str, object], state: Dict[str, object]) -> List[str]:
    return ["classify"]
