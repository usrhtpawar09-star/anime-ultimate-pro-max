"""
Dynamic module loader.
"""
import logging
import importlib
import pkgutil
from core.bot import get_application

logger = logging.getLogger(__name__)

def load_all_modules():
    """Dynamically load all handler modules"""
    app = get_application()
    
    # Import handlers setup
    from handlers import setup_all_handlers
    setup_all_handlers(app)
    
    logger.info("✅ All modules loaded successfully")

# Auto-load on import
load_all_modules()
