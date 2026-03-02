"""
Admin commands for bot management.
"""
import logging
from html import escape
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config import OWNER_ID, SUDO_USERS
from database import db

logger = logging.getLogger(__name__)

def is_admin(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in SUDO_USERS

async def add_character(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add new character to database"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🔐 Admins only!")
        return
    
    if len(context.args) < 4:
        await update.message.reply_text(
            "Usage: /add_char &lt;id&gt; &lt;name&gt; &lt;anime&gt; &lt;img_url&gt; [rarity]"
        )
        return
    
    char_data = {
        "id": context.args[0],
        "name": context.args[1],
        "anime": context.args[2],
        "img_url": context.args[3],
        "rarity": context.args[4] if len(context.args) > 4 else "common"
    }
    
    if await db.add_character(char_data):
        await update.message.reply_text(f"✅ Added: {char_data['name']}")
    else:
        await update.message.reply_text("❌ Failed to add character.")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics"""
    if not is_admin(update.effective_user.id):
        return
    
    users = await db.users.count_documents({})
    chars = await db.characters.count_documents({})
    groups = await db.groups.count_documents({})
    
    stats = (
        f"📊 <b>Bot Statistics</b>\n\n"
        f"👥 Users: {users}\n"
        f"🎴 Characters: {chars}\n"
        f"👥 Groups: {groups}"
    )
    await update.message.reply_text(stats, parse_mode='HTML')

def setup_admin(application):
    """Register admin handlers"""
    application.add_handler(CommandHandler("add_char", add_character))
    application.add_handler(CommandHandler("stats", stats_command))
    logger.info("✅ Admin handlers registered")
