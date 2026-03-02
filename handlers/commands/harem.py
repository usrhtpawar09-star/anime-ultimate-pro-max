"""
/harem command handler with pagination.
"""
import logging
from html import escape
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from database import db
from utils.keyboards import build_harem_keyboard
from utils.formatters import format_collection_entry

logger = logging.getLogger(__name__)

async def harem_command(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0):
    """Display user's collection"""
    user_id = update.effective_user.id
    if update.callback_query:
        # Extract user_id from callback data
        try:
            user_id = int(update.callback_query.data.split(":")[1])
        except:
            pass
    
    data = await db.get_user_collection_paginated(user_id, page=page)
    
    if not data["characters"]:
        msg = "📭 Your harem is empty! Start catching with /guess"
        if update.callback_query:
            await update.callback_query.edit_message_text(msg)
        else:
            await update.message.reply_text(msg)
        return
    
    # Build message
    msg = f"<b>{escape(update.effective_user.first_name)}'s Harem</b>\n"
    msg += f"📊 {data['user_info']['unique_count']} unique | {data['total']} total\n"
    msg += f"🪙 {data['user_info']['coins']} | 💎 {data['user_info']['gems']}\n\n"
    
    # Group by anime
    from itertools import groupby
    chars = sorted(data["characters"], key=lambda x: x["anime"])
    for anime, group in groupby(chars, key=lambda x: x["anime"]):
        group_list = list(group)
        msg += f"<b>{anime}</b> ({len(group_list)})\n"
        for c in group_list[:5]:
            msg += f"• {format_collection_entry(c)}\n"
        if len(group_list) > 5:
            msg += f"  ...+{len(group_list)-5} more\n"
        msg += "\n"
    
    # Keyboard
    keyboard = build_harem_keyboard(user_id, page, data["pages"])
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML'
        )

async def harem_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pagination callbacks"""
    query = update.callback_query
    await query.answer()
    
    try:
        _, user_id, page = query.data.split(":")
        user_id, page = int(user_id), int(page)
        
        if query.from_user.id != user_id:
            await query.answer("⚠️ Not your harem!", show_alert=True)
            return
        
        await harem_command(update, context, page=page)
    except Exception as e:
        logger.error(f"Harem callback error: {e}")

def setup_harem(application):
    """Register harem handlers"""
    application.add_handler(CommandHandler(["harem", "collection"], harem_command))
    application.add_handler(CallbackQueryHandler(harem_callback, pattern="^harem:"))
    logger.info("✅ Harem handlers registered")
