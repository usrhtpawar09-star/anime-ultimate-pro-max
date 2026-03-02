"""
Inline query handlers initialization.
"""

def setup_inline_handlers(application):
    """Register inline handlers"""
    from .search import setup_inline_search
    setup_inline_search(application)

__all__ = ["setup_inline_handlers"]
