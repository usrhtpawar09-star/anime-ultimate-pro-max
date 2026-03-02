"""
General helper functions.
"""
import re

def sanitize_username(username: str) -> str:
    """Clean Telegram username"""
    return re.sub(r'[^a-zA-Z0-9_]', '', username).lower()

def parse_mention(text: str) -> int:
    """Extract user ID from mention"""
    match = re.search(r'tg://user\?id=(\d+)', text)
    if match:
        return int(match.group(1))
    return 0

def safe_int(value, default=0) -> int:
    """Safely convert to int"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
