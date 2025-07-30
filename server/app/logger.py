# Logging configuration for server runtime events
"""
Logger configuration for the Flask app.
"""
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "../server.log")

def setup_logger():
    logger = logging.getLogger("prompt-security")
    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # File handler
    fh = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

logger = setup_logger()
