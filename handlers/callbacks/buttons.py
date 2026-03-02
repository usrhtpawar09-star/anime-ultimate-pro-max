"""
Generic button callback handlers.
"""
import logging
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

logger = logging.getLogger(__name__)

async def handle_generic_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle generic button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    logger.info(f"Callback received: {data}")
    
    # Route based on prefix
    if data.startswith("harem:"):
        from handlers.commands.harem import harem_command
        await harem_command(update, context)
    elif data.startswith("trade:"):
        from handlers.commands.trade import trade_callback
        await trade_callback(update, context)
    # Add more routes as needed

def setup_button_callbacks(application):
    """Register callback handlers"""
    application.add_handler(CallbackQueryHandler(handle_generic_callback))
    logger.info("✅ Callback handlers registered")
