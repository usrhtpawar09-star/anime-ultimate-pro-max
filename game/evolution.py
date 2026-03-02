"""
Character evolution system.
"""
import logging
from typing import Optional, List
from config import EVOLUTION_COST_MULTIPLIER, MIN_EVOLUTION_COPIES
from database import db
from database.models import Character

logger = logging.getLogger(__name__)

class EvolutionSystem:
    """Handle character evolution mechanics"""
    
    async def can_evolve(self, user_id: int, character_id: str) -> tuple[bool, str]:
        """Check if character can be evolved"""
        user = await db.get_user(user_id)
        if not user:
            return False, "User not found"
        
        # Count copies
        copies = sum(c['count'] for c in user.characters if c['id'] == character_id)
        if copies < MIN_EVOLUTION_COPIES:
            return False, f"Need {MIN_EVOLUTION_COPIES} copies (have {copies})"
        
        # Check if evolution exists
        char = await db.get_character(character_id)
        if not char or not char.evolution_chain:
            return False, "This character cannot evolve"
        
        return True, ""
    
    async def evolve_character(self, user_id: int, character_id: str) -> Optional[str]:
        """Evolve character and return new character ID"""
        can_evolve, reason = await self.can_evolve(user_id, character_id)
        if not can_evolve:
            logger.warning(f"Evolution failed for {user_id}: {reason}")
            return None
        
        char = await db.get_character(character_id)
        if not char.evolution_chain:
            return None
        
        # Get next evolution
        next_id = char.evolution_chain[0]
        next_char = await db.get_character(next_id)
        if not next_char:
            return None
        
        # Deduct copies
        user = await db.get_user(user_id)
        updated_chars = []
        for c in user.characters:
            if c['id'] == character_id:
                c['count'] -= MIN_EVOLUTION_COPIES
                if c['count'] > 0:
                    updated_chars.append(c)
            else:
                updated_chars.append(c)
        
        # Add evolved character
        updated_chars.append({"id": next_id, "count": 1, **next_char.model_dump()})
        
        await db.users.update_one(
            {"user_id": user_id},
            {"$set": {"characters": updated_chars}}
        )
        
        logger.info(f"User {user_id} evolved {character_id} -> {next_id}")
        return next_id
