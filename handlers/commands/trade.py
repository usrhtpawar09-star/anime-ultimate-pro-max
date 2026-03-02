"""
/trade command handler with escrow.
"""
import logging
import uuid
from datetime import datetime, timedelta
from html import escape
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from config import TRADE_EXPIRY_MINUTES, ENABLE_TRADING
from database import db
from database.models import TradeOffer
from game import economy

logger = logging.getLogger(__name__)

if not ENABLE_TRADING:
    logger.info("⚠️ Trading disabled in config")

async def trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiate trade"""
    if not ENABLE_TRADING:
        await update.message.reply_text("🔒 Trading is currently disabled.")
        return
    
    user = update.effective_user
    chat = update.effective_chat
    
    if chat.type == "private":
        await update.message.reply_text("❌ Trade in groups only!")
        return
    
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /trade @username &lt;character_id&gt;")
        return
    
    # Parse args (simplified)
    target = context.args[0].lstrip('@')
    char_id = context.args[1]
    
    # Check if character exists in user's collection
    user_data = await db.get_user(user.id)
    if not user_data or not any(c['id'] == char_id for c in user_data.characters):
        await update.message.reply_text("❌ You don't have that character!")
        return
    
    # Create trade offer (simplified - real impl needs user resolution)
    trade = TradeOffer(
        trade_id=str(uuid.uuid4())[:12],
        sender_id=user.id,
        receiver_id=0,  # TODO: Resolve username to ID
        chat_id=chat.id,
        offered={char_id: 1},
        requested={},
        expires_at=datetime.utcnow() + timedelta(minutes=TRADE_EXPIRY_MINUTES)
    )
    
    if await db.create_trade(trade):
        keyboard = [[
            InlineKeyboardButton("✅ Accept", callback_data=f"trade:accept:{trade.trade_id}"),
            InlineKeyboardButton("❌ Decline", callback_data=f"trade:reject:{trade.trade_id}")
        ]]
        await update.message.reply_text(
            f"🔄 Trade offer sent!\n\n"
            f"Offering: {char_id}\n"
            f"Expires in {TRADE_EXPIRY_MINUTES} min",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("❌ Failed to create trade.")

async def trade_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle trade accept/reject"""
    query = update.callback_query
    await query.answer()
    
    action, trade_id = query.data.split(":")[1], query.data.split(":")[2]
    trade = await db.get_trade(trade_id)
    
    if not trade or trade.status != "pending":
        await query.edit_message_text("⚠️ Trade expired or invalid.")
        return
    
    if action == "accept":
        # Process trade (simplified)
        await db.update_trade_status(trade_id, "completed")
        await query.edit_message_text("✅ Trade completed!")
    elif action == "reject":
        await db.update_trade_status(trade_id, "rejected")
        await query.edit_message_text("❌ Trade declined.")

def setup_trade(application):
    """Register trade handlers"""
    if ENABLE_TRADING:
        application.add_handler(CommandHandler("trade", trade_command))
        application.add_handler(CallbackQueryHandler(trade_callback, pattern="^trade:"))
        logger.info("✅ Trade handlers registered")
