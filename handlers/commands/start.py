"""
/start and /help command handlers.
"""
import logging
import random
from html import escape
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from config import BOT_USERNAME, SUPPORT_CHAT, UPDATE_CHAT, DEFAULT_PHOTOS
from database import db
from utils.keyboards import build_main_keyboard

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    chat_type = update.effective_chat.type
    
    # Track user
    if not await db.get_user(user.id):
        await db.create_user(user.id, user.username or "", user.first_name)
    
    if chat_type == "private":
        caption = (
            f"👋 <b>Hey {escape(user.first_name)}!</b>\n\n"
            f"I'm <b>{BOT_USERNAME}</b> - Your ultimate character collector! 🎴\n\n"
            f"🎮 <b>How to play:</b>\n"
            f"• Add me to your group\n"
            f"• I send random characters every 100 messages\n"
            f"• Use /guess &lt;name&gt; to catch them\n"
            f"• Build your harem with /harem\n\n"
            f"Use /help for all commands!"
        )
        keyboard = build_main_keyboard(user.id, is_private=True)
    else:
        caption = f"✅ <b>{BOT_USERNAME} is ready!</b>\nUse /guess to catch characters."
        keyboard = build_main_keyboard(user.id, is_private=False)
    
    await update.message.reply_photo(
        photo=random.choice(DEFAULT_PHOTOS),
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "<b>📚 Command Guide:</b>\n\n"
        "<b>🎮 Game:</b>\n"
        "/guess &lt;name&gt; - Guess character name\n"
        "/harem - View your collection\n"
        "/top - Global leaderboard\n\n"
        "<b>💰 Economy:</b>\n"
        "/trade @user &lt;id&gt; - Trade characters\n"
        "/balance - Check coins/gems\n\n"
        "<b>⚙️ Other:</b>\n"
        "/help - This message\n"
        "/start - Restart bot"
    )
    await update.message.reply_text(help_text, parse_mode='HTML')

def setup_start(application):
    """Register start/help handlers"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    logger.info("✅ Start/Help handlers registered")
