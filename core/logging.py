"""
Professional logging setup with file rotation.
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import LOG_LEVEL

def setup_logger(name: str, log_file: str = "bot.log") -> logging.Logger:
    """Create logger with console and rotating file handler"""
    
    Path("logs").mkdir(exist_ok=True)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # File handler with rotation (10MB max, 5 backups)
    file_handler = RotatingFileHandler(
        f"logs/{log_file}",
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
