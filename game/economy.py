"""
Economy system for coins, gems, and rewards.
"""
import logging
from config import REWARD_COINS, REWARD_GEMS, TRADE_FEE_PERCENT
from database import db

logger = logging.getLogger(__name__)

class EconomyManager:
    """Manage in-game economy"""
    
    async def calculate_guess_reward(self, rarity: str) -> dict:
        """Calculate rewards for successful guess"""
        return {
            "coins": REWARD_COINS.get(rarity, 10),
            "gems": REWARD_GEMS.get(rarity, 0),
            "xp": REWARD_COINS.get(rarity, 10) * 2
        }
    
    async def calculate_trade_fee(self, total_value: int) -> int:
        """Calculate trade fee"""
        return int(total_value * TRADE_FEE_PERCENT / 100)
    
    async def can_afford(self, user_id: int, coins: int = 0, gems: int = 0) -> bool:
        """Check if user has enough currency"""
        user = await db.get_user(user_id)
        if not user:
            return False
        return user.coins >= coins and user.gems >= gems
    
    async def deduct_currency(self, user_id: int, coins: int = 0, gems: int = 0) -> bool:
        """Deduct currency from user"""
        if not await self.can_afford(user_id, coins, gems):
            return False
        update = {}
        if coins > 0:
            update["$inc"] = {"coins": -coins}
        if gems > 0:
            update["$inc"] = update.get("$inc", {})
            update["$inc"]["gems"] = -gems
        if update:
            await db.users.update_one({"user_id": user_id}, update)
            return True
        return False
