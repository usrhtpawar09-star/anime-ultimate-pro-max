"""
/guess command handler with full logic.
"""
import logging
from html import escape
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from config import GUESS_COOLDOWN
from database import db
from game import validator, economy
from utils.keyboards import build_guess_keyboard
from utils.formatters import format_character_info

logger = logging.getLogger(__name__)
_cooldowns = {}

async def guess_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /guess command"""
    user = update.effective_user
    chat = update.effective_chat
    
    if chat.type == "private":
        await update.message.reply_text("❌ Use this in groups!")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /guess &lt;character_name&gt;")
        return
    
    # Cooldown check
    if user.id in _cooldowns:
        await update.message.reply_text(f"⏳ Wait {GUESS_COOLDOWN}s!")
        return
    
    guess = " ".join(context.args)
    active = await db.get_active_character(chat.id)
    
    if not active:
        await update.message.reply_text("❌ No character active!")
        return
    
    # Validate
    is_correct, feedback = validator.validate(guess, active)
    
    if is_correct:
        # Check double-guess
        if await db.mark_as_guessed(chat.id, user.id):
            await _handle_success(update, context, user, chat, active)
        else:
            await update.message.reply_text("⚡ Already caught!")
    else:
        await update.message.reply_text(feedback, parse_mode='Markdown')
        _set_cooldown(user.id)

async def _handle_success(update, context, user, chat, character):
    """Process successful guess"""
    # Calculate rewards
    rewards = await economy.calculate_guess_reward(character.rarity.value)
    
    # Add to collection
    await db.add_character_to_user(user.id, character)
    if rewards["coins"] > 0:
        await db.add_currency(user.id, coins=rewards["coins"])
    if rewards["gems"] > 0:
        await db.add_currency(user.id, gems=rewards["gems"])
    
    # Build response
    keyboard = build_guess_keyboard(user.id, character.id)
    caption = (
        f"🎉 <b>Correct, {escape(user.first_name)}!</b>\n\n"
        f"{format_character_info(character)}\n\n"
        f"✨ Rewards: 🪙 +{rewards['coins']}" +
        (f" 💎 +{rewards['gems']}" if rewards['gems'] else "")
    )
    
    await update.message.reply_photo(
        photo=character.img_url,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
    
    # Clear game
    await db.clear_active_character(chat.id)

def _set_cooldown(user_id: int):
    _cooldowns[user_id] = True
    import asyncio
    asyncio.get_event_loop().call_later(GUESS_COOLDOWN, lambda: _cooldowns.pop(user_id, None))

def setup_guess(application):
    """Register guess handler"""
    application.add_handler(CommandHandler(
        ["guess", "catch", "collect", "grab", "protecc"],
        guess_command
    ))
    logger.info("✅ Guess handler registered")
