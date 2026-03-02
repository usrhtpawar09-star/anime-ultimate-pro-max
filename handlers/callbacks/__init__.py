"""
Callback query handlers initialization.
"""

def setup_callback_handlers(application):
    """Register all callback handlers"""
    from .buttons import setup_button_callbacks
    setup_button_callbacks(application)

__all__ = ["setup_callback_handlers"]
