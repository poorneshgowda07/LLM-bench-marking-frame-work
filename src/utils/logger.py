"""Structured logging for the LLM Benchmarking Framework."""
import logging
import sys
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console

console = Console()

def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Get a configured logger with rich formatting."""
    log_level = level or "INFO"
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )
    logger = logging.getLogger(name)
    return logger


logger = get_logger("llm_benchmark")
