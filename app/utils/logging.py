# Folder: /app/utils
"""Lightweight logging configuration used by the MyMia backend.

This module exposes a function to configure logging for the app and a helper `get_logger`.
"""
import logging
from typing import Optional


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))


def get_logger(name: Optional[str] = None) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
