"""
Character spawn logic with rates and anti-spam.
"""
import logging
import random
from datetime import datetime, timedelta
from typing import Optional, Dict
from config import MESSAGE_THRESHOLD, RARITY_WEIGHTS
from database import db
from database.models import Character

logger = logging.getLogger(__name__)

class CharacterSpawner:
    """Manages character spawning in groups"""
    
    _message_counts: Dict[int, Dict] = {}
    
    async def should_spawn(self, chat_id: int) -> bool:
        """Determine if character should spawn"""
        threshold = await self._get_threshold(chat_id)
        
        if chat_id not in self._message_counts:
            self._message_counts[chat_id] = {'count': 0, 'last_reset': datetime.utcnow()}
        
        self._message_counts[chat_id]['count'] += 1
        
        if self._message_counts[chat_id]['count'] >= threshold:
            self._message_counts[chat_id]['count'] = 0
            return True
        return False
    
    async def _get_threshold(self, chat_id: int) -> int:
        """Get message threshold for group (with overrides)"""
        settings = await db.get_group_settings(chat_id)
        return settings.message_threshold if settings and settings.message_threshold else MESSAGE_THRESHOLD
    
    async def spawn_character(self, chat_id: int, excluded_ids: list = None) -> Optional[Character]:
        """Spawn a random character"""
        # Get allowed rarities from group settings
        settings = await db.get_group_settings(chat_id)
        
        # Select rarity based on weights
        rarity = random.choices(
            list(RARITY_WEIGHTS.keys()),
            weights=list(RARITY_WEIGHTS.values())
        )[0]
        
        character = await db.get_random_character(
            exclude_ids=excluded_ids,
            rarity=rarity
        )
        
        if character:
            logger.info(f"Spawned {character.name} ({character.rarity.value}) in chat {chat_id}")
            await db.set_active_character(chat_id, character)
        
        return character
    
    def reset_counter(self, chat_id: int):
        """Manually reset message counter"""
        if chat_id in self._message_counts:
            self._message_counts[chat_id] = {'count': 0, 'last_reset': datetime.utcnow()}
    
    def get_progress(self, chat_id: int) -> float:
        """Get spawn progress (0.0 to 1.0)"""
        if chat_id not in self._message_counts:
            return 0.0
        threshold = MESSAGE_THRESHOLD
        return min(1.0, self._message_counts[chat_id]['count'] / threshold)
