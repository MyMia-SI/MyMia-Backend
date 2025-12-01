# Folder: /app/workflows
"""Mold inspection workflow definition.

This module defines the execution steps for `mold_inspection` in a minimal, declarative way.
"""
from typing import Dict, List


WORKFLOW_NAME = "mold_inspection"
VERSION = "0.1"
DESCRIPTION = "Vision -> Moisture -> Protocol: Analyze images and produce a remediation protocol."


def get_steps(context: Dict[str, object], state: Dict[str, object]) -> List[str]:
    """Return the list of step names for mold inspection."""
    return ["vision", "moisture", "protocol"]
