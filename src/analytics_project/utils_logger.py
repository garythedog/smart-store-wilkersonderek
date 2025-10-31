from __future__ import annotations
import logging
from pathlib import Path

# Project-level directory references
PROJECT_DIR = Path(__file__).resolve().parents[2]
LOG_FILE = PROJECT_DIR / "project.log"

_LOGGERS: dict[str, logging.Logger] = {}


def get_logger(name: str = "analytics_project") -> logging.Logger:
    """
    Create or return a shared logger configured to output to both the console and project.log.

    Parameters
    ----------
    name : str, optional
        The name of the logger, by default "analytics_project".

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Avoid duplicate logs

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _LOGGERS[name] = logger
    return logger
