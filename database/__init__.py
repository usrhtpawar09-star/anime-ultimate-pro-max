"""
Database module initialization.
"""
from .mongodb import MongoDB
from .models import Character, UserCollection, GroupSettings, TradeOffer

# Global database instance
db = MongoDB()

__all__ = ["db", "Character", "UserCollection", "GroupSettings", "TradeOffer"]
