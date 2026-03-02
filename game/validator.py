"""
Advanced guess validation with fuzzy matching.
"""
import re
import logging
from typing import Tuple
from difflib import SequenceMatcher
from database.models import Character

logger = logging.getLogger(__name__)

class GuessValidator:
    """Sophisticated guess validation"""
    
    IGNORE_CHARS = set('()[]{}<>!@#$%^&*_=+|\\;:\'",.?/~`')
    
    TYPO_FIXES = {
        'narutoo': 'naruto', 'sasukee': 'sasuke', 'gokuu': 'goku',
        'luffi': 'luffy', 'zoroa': 'zoro'
    }
    
    def __init__(self, min_similarity: float = 0.7):
        self.min_similarity = min_similarity
    
    def sanitize(self, text: str) -> str:
        """Normalize guess text"""
        text = text.lower().strip()
        text = ''.join(c for c in text if c not in self.IGNORE_CHARS)
        text = re.sub(r'\s+', ' ', text)
        for typo, correct in self.TYPO_FIXES.items():
            text = text.replace(typo, correct)
        return text
    
    def similarity(self, s1: str, s2: str) -> float:
        """Calculate string similarity"""
        if not s1 or not s2:
            return 0.0
        return SequenceMatcher(None, s1, s2).ratio()
    
    def validate(self, guess: str, character: Character) -> Tuple[bool, str]:
        """Validate guess and return (is_correct, feedback)"""
        g = self.sanitize(guess)
        name = self.sanitize(character.name)
        
        # Exact match
        if g == name:
            return True, "Perfect! 🎯"
        
        # Alias match
        if g in [self.sanitize(a) for a in character.aliases]:
            return True, "Correct! (alias) ✨"
        
        # Partial match for multi-word names
        if len(name.split()) >= 2:
            name_words = set(name.split())
            guess_words = set(g.split())
            if guess_words and guess_words.issubset(name_words):
                return True, "Good! (partial) 👍"
        
        # Fuzzy match
        sim = self.similarity(g, name)
        if sim >= self.min_similarity:
            return True, f"Close! ({sim*100:.0f}%) ✅"
        
        # Wrong - helpful feedback
        if sim > 0.5:
            return False, f"🤔 Almost! Did you mean **{character.name}**?"
        return False, f"❌ Try: **{character.name}** from {character.anime}"
    
    def detect_spam(self, guesses: list) -> bool:
        """Detect spam patterns"""
        if len(guesses) < 5:
            return False
        recent = guesses[-10:]
        # All same guess
        if len(set(recent)) == 1:
            return True
        # Single char spam
        if all(len(g) == 1 for g in recent[-5:]):
            return True
        return False
