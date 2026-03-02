"""
Text formatting utilities.
"""
from html import escape
from database.models import Character

def format_character_info(char: Character) -> str:
    """Format character for display"""
    return (
        f"🌸 <b>{escape(char.name)}</b> {char.rarity.emoji}\n"
        f"🎬 <b>Anime:</b> {escape(char.anime)}\n"
        f"🆔 <b>ID:</b> <code>{char.id}</code>"
    )

def format_collection_entry(char: dict) -> str:
    """Format collection entry"""
    return f"{char['name']} ×{char.get('count', 1)}"

def truncate(text: str, max_len: int = 100) -> str:
    """Truncate text with ellipsis"""
    return text if len(text) <= max_len else text[:max_len-3] + "..."
