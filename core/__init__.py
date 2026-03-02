"""
Core module initialization.
"""
from .logging import setup_logger
from .exceptions import (
    BotException, ConfigurationError, DatabaseError,
    CharacterNotFoundError, UserNotFoundError, TradeError
)

logger = setup_logger("core")

__all__ = [
    "logger",
    "BotException", "ConfigurationError", "DatabaseError",
    "CharacterNotFoundError", "UserNotFoundError", "TradeError"
]
