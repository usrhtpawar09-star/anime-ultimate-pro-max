"""
Pydantic models for type-safe database operations.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

class Rarity(Enum):
    COMMON = "common"
    MEDIUM = "medium"
    RARE = "rare"
    LEGENDARY = "legendary"
    MYTHICAL = "mythical"
    
    @property
    def emoji(self) -> str:
        return {'common': '⚪️', 'medium': '🟢', 'rare': '🟣', 
                'legendary': '🟡', 'mythical': '🔴'}[self.value]
    
    @property
    def color(self) -> str:
        return {'common': '#A9A9A9', 'medium': '#90EE90', 'rare': '#DDA0DD',
                'legendary': '#FFD700', 'mythical': '#FF4500'}[self.value]

class Character(BaseModel):
    id: str
    name: str
    anime: str
    img_url: str
    rarity: Rarity = Rarity.COMMON
    description: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    stats: Dict[str, Any] = Field(default_factory=dict)
    evolution_chain: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('aliases')
    def lowercase_aliases(cls, v):
        return [alias.lower().strip() for alias in v]
    
    def matches_guess(self, guess: str) -> bool:
        """Check if user guess matches this character"""
        guess = guess.lower().strip()
        name = self.name.lower()
        if guess == name:
            return True
        if guess in self.aliases:
            return True
        # Partial match for multi-word names        if len(name.split()) >= 2:
            name_words = set(name.split())
            guess_words = set(guess.split())
            if guess_words and guess_words.issubset(name_words):
                return True
        return False

class UserCollection(BaseModel):
    user_id: int
    username: Optional[str] = None
    first_name: str
    characters: List[Dict[str, Any]] = Field(default_factory=list)
    favorites: List[str] = Field(default_factory=list)
    coins: int = Field(default=0, ge=0)
    gems: int = Field(default=0, ge=0)
    total_guesses: int = Field(default=0, ge=0)
    correct_guesses: int = Field(default=0, ge=0)
    join_date: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def accuracy(self) -> float:
        if self.total_guesses == 0:
            return 0.0
        return (self.correct_guesses / self.total_guesses) * 100
    
    @property
    def unique_count(self) -> int:
        return len({c['id'] for c in self.characters})

class GroupSettings(BaseModel):
    chat_id: int
    title: str
    enabled: bool = True
    message_threshold: Optional[int] = None
    language: str = 'en'
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TradeOffer(BaseModel):
    trade_id: str
    sender_id: int
    receiver_id: int
    chat_id: int
    offered: Dict[str, int] = Field(default_factory=dict)
    requested: Dict[str, int] = Field(default_factory=dict)
    status: str = 'pending'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    
    @validator('expires_at')    def must_be_future(cls, v):
        if v <= datetime.utcnow():
            raise ValueError('Expiry must be in future')
        return v
