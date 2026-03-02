"""
Game engine module initialization.
"""
from .spawner import CharacterSpawner
from .validator import GuessValidator
from .economy import EconomyManager
from .evolution import EvolutionSystem
from .events import EventManager

spawner = CharacterSpawner()
validator = GuessValidator()
economy = EconomyManager()
evolution = EvolutionSystem()
events = EventManager()

__all__ = ["spawner", "validator", "economy", "evolution", "events"]
