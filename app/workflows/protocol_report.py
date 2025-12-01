# Folder: /app/workflows
"""Protocol report workflow definition (GPT-driven writing of remediation protocol).
"""
from typing import Dict, List


WORKFLOW_NAME = "protocol_report"
VERSION = "0.1"
DESCRIPTION = "Generate protocol report from collected observations."


def get_steps(context: Dict[str, object], state: Dict[str, object]) -> List[str]:
    return ["protocol"]
