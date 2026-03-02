"""
Inline search handler for character lookup.
"""
import logging
import re
from telegram import Update, InlineQueryResultPhoto
from telegram.ext import InlineQueryHandler, ContextTypes
from database import db

logger = logging.getLogger(__name__)

async def inline_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline character search"""
    query = update.inline_query.query
    offset = int(update.inline_query.offset) if update.inline_query.offset else 0
    
    if query.startswith("collection:"):
        # User collection search
        user_id = query.split(":")[1].split()[0]
        search_term = " ".join(query.split(":")[1].split()[1:])
        
        user = await db.get_user(int(user_id))
        if not user:
            await update.inline_query.answer([], cache_time=30)
            return
        
        chars = [c for c in user.characters if search_term.lower() in c['name'].lower()]
    else:
        # Global character search
        if query:
            regex = re.compile(query, re.IGNORECASE)
            chars = await db.search_characters(query, limit=50)
        else:
            chars = await db.search_characters("", limit=50)
    
    # Build results
    results = []
    for char in chars[offset:offset+50]:
        caption = (
            f"🌸 {char.name}\n"
            f"🎬 {char.anime}\n"
            f"{char.rarity.emoji} {char.rarity.value}"
        )
        results.append(
            InlineQueryResultPhoto(
                id=f"{char.id}_{offset}",
                photo_url=char.img_url,
                thumbnail_url=char.img_url,
                caption=caption,
                parse_mode='HTML'
            )
        )
    
    next_offset = str(offset + 50) if len(chars) > offset + 50 else ""
    await update.inline_query.answer(results, next_offset=next_offset, cache_time=30)

def setup_inline_search(application):
    """Register inline handler"""
    application.add_handler(InlineQueryHandler(inline_search))
    logger.info("✅ Inline search handler registered")
