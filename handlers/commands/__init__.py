"""
Command handlers initialization.
"""

def setup_command_handlers(application):
    """Register all command handlers"""
    from .start import setup_start
    from .guess import setup_guess
    from .harem import setup_harem
    from .trade import setup_trade
    from .admin import setup_admin
    
    setup_start(application)
    setup_guess(application)
    setup_harem(application)
    setup_trade(application)
    setup_admin(application)

__all__ = ["setup_command_handlers"]
