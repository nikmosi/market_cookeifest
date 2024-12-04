import sys

from loguru import logger

from .config import config

__all__ = ["config"]

logger.remove()
logger.add(sys.stderr, colorize=True)
