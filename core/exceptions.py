"""
Custom exception classes for the bot.
"""

class BotException(Exception):
    """Base exception for all bot errors"""
    pass

class ConfigurationError(BotException):
    """Raised when configuration is invalid"""
    pass

class DatabaseError(BotException):
    """Raised when database operation fails"""
    pass

class CharacterNotFoundError(BotException):
    """Raised when character is not found in database"""
    pass

class UserNotFoundError(BotException):
    """Raised when user is not found in database"""
    pass

class GuessValidationError(BotException):
    """Raised when guess validation fails"""
    pass

class TradeError(BotException):
    """Raised when trade operation fails"""
    pass

class InsufficientFundsError(BotException):
    """Raised when user doesn't have enough currency"""
    pass

class RateLimitError(BotException):
    """Raised when user exceeds rate limit"""
    pass
