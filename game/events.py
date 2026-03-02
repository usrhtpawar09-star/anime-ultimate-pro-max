"""
Limited-time events system.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional, List
from config import EVENT_BONUS_MULTIPLIER

logger = logging.getLogger(__name__)

class EventManager:
    """Manage time-limited events"""
    
    _active_events: List[dict] = []
    
    def register_event(self, event_ dict):
        """Register a new event"""
        self._active_events.append({
            **event_data,
            "start": datetime.fromisoformat(event_data["start"]),
            "end": datetime.fromisoformat(event_data["end"])
        })
        logger.info(f"🎉 Event registered: {event_data['name']}")
    
    def get_active_events(self) -> List[dict]:
        """Get currently active events"""
        now = datetime.utcnow()
        return [e for e in self._active_events if e["start"] <= now <= e["end"]]
    
    def get_reward_multiplier(self, character_rarity: str) -> float:
        """Get reward multiplier from active events"""
        multiplier = 1.0
        for event in self.get_active_events():
            if event.get("bonus_rarity") == character_rarity:
                multiplier = max(multiplier, event.get("multiplier", EVENT_BONUS_MULTIPLIER))
        return multiplier
    
    def is_event_character(self, character_id: str) -> bool:
        """Check if character is event-exclusive"""
        now = datetime.utcnow()
        for event in self._active_events:
            if event["start"] <= now <= event["end"]:
                if character_id in event.get("exclusive_chars", []):
                    return True
        return False
