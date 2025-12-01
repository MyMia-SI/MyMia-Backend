# Folder: /app/actions
"""Legacy action wrappers (optional). Historically used to group operations that predate the Services layer.

Each action exposes an async `handle(payload, context)` function and returns a structured JSON result.
"""

from . import (
	job_intake,
	media_upload,
	ai_mold_analysis,
	moisture_mapping,
	virtual_assessment,
	generate_report,
	property_lookup,
	weather_risk_assessment,
	invoice_create,
	schedule_event,
	email_summary,
	job_classifier,
)

__all__ = [
	"job_intake",
	"media_upload",
	"ai_mold_analysis",
	"moisture_mapping",
	"virtual_assessment",
	"generate_report",
	"property_lookup",
	"weather_risk_assessment",
	"invoice_create",
	"schedule_event",
	"email_summary",
	"job_classifier",
]
