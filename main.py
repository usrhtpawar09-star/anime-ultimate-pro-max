"""
Main entry point - Production Ready.
"""
import asyncio
import signal
import sys
import logging
from core.bot import BotManager, get_application
from database import db
from database.redis import cache
from core.logging import setup_logger
from config import LOG_LEVEL

logger = setup_logger("main")

shutdown_event = asyncio.Event()

def handle_shutdown(signum, frame):
    """Handle graceful shutdown"""
    logger.info(f"🛑 Signal {signum} received, shutting down...")
    shutdown_event.set()

async def main():
    """Main application loop"""
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    try:
        # Initialize Redis cache (optional)
        await cache.connect()
        
        # Initialize database indexes
        await db.init_indexes()
        logger.info("🗄️ Database ready")
        
        # Start Pyrogram client
        await BotManager.start_all()
        
        # Get PTB application
        app = get_application()
        
        logger.info("🚀 Bot starting...")
        
        # Run polling
        await app.initialize()
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        
        # Keep alive
        await shutdown_event.wait()
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await cleanup()

async def cleanup():
    """Cleanup resources"""
    logger.info("🧹 Cleaning up...")
    await cache.close()
    await BotManager.stop_all()
    app = get_application()
    await app.stop()
    await app.shutdown()
    logger.info("✅ Cleanup complete")

if __name__ == "__main__":
    asyncio.run(main())
