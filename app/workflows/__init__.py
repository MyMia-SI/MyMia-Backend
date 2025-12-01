# Folder: /app/workflows
"""Package for AI workflow definitions.

Workflows should define a single interface for step definitions and to be consumable by the Orchestrator.
"""

from . import mold_inspection, virtual_assessment, protocol_report, invoice_summary, job_classifier

__all__ = [
	"mold_inspection",
	"virtual_assessment",
	"protocol_report",
	"invoice_summary",
	"job_classifier",
]
