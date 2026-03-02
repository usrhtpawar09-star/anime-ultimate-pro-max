"""
Handlers module initialization.
"""

def setup_all_handlers(application):
    """Register all command handlers"""
    from handlers.commands import setup_command_handlers
    from handlers.callbacks import setup_callback_handlers
    from handlers.inline import setup_inline_handlers
    
    setup_command_handlers(application)
    setup_callback_handlers(application)
    setup_inline_handlers(application)

__all__ = ["setup_all_handlers"]
