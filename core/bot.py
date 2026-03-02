"""
Bot instance management.
"""
from telegram.ext import Application
from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH
from core.logging import setup_logger

logger = setup_logger("bot")

class BotManager:
    """Manage bot instances"""
    
    _ptb_app = None
    _pyrogram_client = None
    
    @classmethod
    def get_ptb_app(cls) -> Application:
        """Get python-telegram-bot Application instance"""
        if cls._ptb_app is None:
            cls._ptb_app = Application.builder().token(BOT_TOKEN).build()
            logger.info("✅ PTB Application initialized")
        return cls._ptb_app
    
    @classmethod
    def get_pyrogram_client(cls) -> Client:
        """Get Pyrogram Client instance"""
        if cls._pyrogram_client is None:
            cls._pyrogram_client = Client(
                "bot_session",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=BOT_TOKEN,
                workers=50,
                no_updates=True,
                in_memory=True
            )
            logger.info("✅ Pyrogram Client initialized")
        return cls._pyrogram_client
    
    @classmethod
    async def start_all(cls):
        """Start all bot clients"""
        client = cls.get_pyrogram_client()
        await client.start()
        logger.info("🚀 All bot clients started")
    
    @classmethod
    async def stop_all(cls):
        """Stop all bot clients"""
        client = cls.get_pyrogram_client()
        if client.is_connected:
            await client.stop()
        logger.info("🛑 All bot clients stopped")

# Global accessor
def get_application() -> Application:
    return BotManager.get_ptb_app()

def get_pyrogram() -> Client:
    return BotManager.get_pyrogram_client()
