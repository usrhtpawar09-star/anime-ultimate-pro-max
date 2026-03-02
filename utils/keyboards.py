"""
Inline keyboard builder utilities.
"""
from telegram import InlineKeyboardButton
from config import BOT_USERNAME, SUPPORT_CHAT, UPDATE_CHAT

def build_main_keyboard(user_id: int, is_private: bool) -> list:
    """Build main menu keyboard"""
    keyboard = []
    
    if is_private:
        keyboard.append([
            InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=new")
        ])
    
    keyboard.append([
        InlineKeyboardButton("💬 Support", url=f"https://t.me/{SUPPORT_CHAT}"),
        InlineKeyboardButton("📢 Updates", url=f"https://t.me/{UPDATE_CHAT}")
    ])
    
    if is_private:
        keyboard.append([
            InlineKeyboardButton("👤 My Harem", callback_data=f"harem:{user_id}:0"),
            InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")
        ])
    
    return keyboard

def build_guess_keyboard(user_id: int, char_id: str) -> list:
    """Build keyboard after successful guess"""
    return [[
        InlineKeyboardButton("📦 View Harem", callback_data=f"harem:{user_id}:0"),
        InlineKeyboardButton("⭐ Favorite", callback_data=f"fav:{char_id}")
    ]]

def build_harem_keyboard(user_id: int, page: int, total_pages: int) -> list:
    """Build pagination keyboard for harem"""
    keyboard = []
    
    if total_pages > 1:
        nav = []
        if page > 0:
            nav.append(InlineKeyboardButton("⬅️", callback_data=f"harem:{user_id}:{page-1}"))
        nav.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data="noop"))
        if page < total_pages - 1:
            nav.append(InlineKeyboardButton("➡️", callback_data=f"harem:{user_id}:{page+1}"))
        keyboard.append(nav)
    
    keyboard.append([
        InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat=f"collection.{user_id}")
    ])
    
    return keyboard
