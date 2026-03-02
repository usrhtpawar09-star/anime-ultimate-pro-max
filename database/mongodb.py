"""
MongoDB implementation with complete methods.
"""
import logging
from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, DB_NAME, RARITY_WEIGHTS
from .models import Character, UserCollection, GroupSettings, TradeOffer
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGODB_URL)
        self.db = self.client[DB_NAME]
        self.characters = self.db["characters"]
        self.users = self.db["users"]
        self.groups = self.db["groups"]
        self.active_games = self.db["active_games"]
        self.trades = self.db["trades"]
    
    async def init_indexes(self):
        """Create all necessary indexes"""
        await self.characters.create_index("id", unique=True)
        await self.characters.create_index([("anime", 1), ("name", 1)])
        await self.characters.create_index("rarity")
        
        await self.users.create_index("user_id", unique=True)
        await self.groups.create_index("chat_id", unique=True)
        await self.active_games.create_index("chat_id", unique=True)
        await self.active_games.create_index("expires_at", expireAfterSeconds=0)
        await self.trades.create_index("trade_id", unique=True)
        logger.info("✅ Database indexes created")
    
    # === Character Operations ===
    async def add_character(self, char_ Dict[str, Any]) -> bool:
        try:
            await self.characters.insert_one(char_data)
            return True
        except Exception as e:
            logger.error(f"Failed to add character: {e}")
            return False
    
    async def get_character(self, char_id: str) -> Optional[Character]:
        doc = await self.characters.find_one({"id": char_id})
        return Character(**doc) if doc else None
    
    async def get_random_character(self, exclude_ids: List[str] = None,                                   rarity: Optional[str] = None) -> Optional[Character]:
        query = {}
        if exclude_ids:
            query["id"] = {"$nin": exclude_ids}
        if rarity:
            query["rarity"] = rarity
        elif random.random() < 0.3:  # 30% chance for weighted rarity
            rarity = random.choices(
                list(RARITY_WEIGHTS.keys()),
                weights=list(RARITY_WEIGHTS.values())
            )[0]
            query["rarity"] = rarity
        
        count = await self.characters.count_documents(query)
        if count == 0:
            return None
        
        skip = random.randint(0, max(0, count - 1))
        cursor = self.characters.find(query).skip(skip).limit(1)
        docs = await cursor.to_list(1)
        return Character(**docs[0]) if docs else None
    
    async def search_characters(self, query: str, limit: int = 50) -> List[Character]:
        import re
        regex = re.compile(query, re.IGNORECASE)
        cursor = self.characters.find({
            "$or": [
                {"name": regex},
                {"anime": regex},
                {"aliases": regex}
            ]
        }).limit(limit)
        return [Character(**doc) async for doc in cursor]
    
    # === User Operations ===
    async def get_user(self, user_id: int) -> Optional[UserCollection]:
        doc = await self.users.find_one({"user_id": user_id})
        return UserCollection(**doc) if doc else None
    
    async def create_user(self, user_id: int, username: str, first_name: str) -> UserCollection:
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "characters": [],
            "favorites": [],
            "coins": 0,
            "gems": 0,
            "total_guesses": 0,
            "correct_guesses": 0,            "join_date": datetime.utcnow(),
            "last_active": datetime.utcnow()
        }
        await self.users.insert_one(user_data)
        return UserCollection(**user_data)
    
    async def add_character_to_user(self, user_id: int, character: Character, count: int = 1) -> bool:
        user = await self.get_user(user_id)
        if not user:
            user = await self.create_user(user_id, "", "User")
        
        char_data = character.model_dump()
        char_data["count"] = count
        
        # Check if character already exists
        updated = False
        for char in user.characters:
            if char["id"] == character.id:
                char["count"] = char.get("count", 1) + count
                updated = True
                break
        
        if not updated:
            user.characters.append(char_data)
        
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"characters": user.characters, "last_active": datetime.utcnow()}}
        )
        return True
    
    async def add_currency(self, user_id: int, coins: int = 0, gems: int = 0) -> bool:
        update = {}
        if coins > 0:
            update["$inc"] = {"coins": coins}
        if gems > 0:
            update["$inc"] = update.get("$inc", {})
            update["$inc"]["gems"] = gems
        if update:
            update["$set"] = {"last_active": datetime.utcnow()}
            result = await self.users.update_one({"user_id": user_id}, update)
            return result.modified_count > 0
        return False
    
    async def get_user_collection_paginated(self, user_id: int, page: int = 0, per_page: int = 15) -> Dict:
        user = await self.get_user(user_id)
        if not user:
            return {"characters": [], "total": 0, "page": 0, "pages": 0}
        
        chars = user.characters        total = len(chars)
        pages = (total + per_page - 1) // per_page
        page = max(0, min(page, pages - 1))
        
        start = page * per_page
        end = start + per_page
        
        return {
            "characters": chars[start:end],
            "total": total,
            "page": page,
            "pages": pages,
            "user_info": {
                "coins": user.coins,
                "gems": user.gems,
                "accuracy": user.accuracy,
                "unique_count": user.unique_count
            }
        }
    
    # === Active Game Operations ===
    async def set_active_character(self, chat_id: int, character: Character, expires_in: int = 300):
        await self.active_games.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "character": character.model_dump(),
                    "expires_at": datetime.utcnow() + timedelta(seconds=expires_in),
                    "guessed_by": None
                }
            },
            upsert=True
        )
    
    async def get_active_character(self, chat_id: int) -> Optional[Character]:
        game = await self.active_games.find_one({"chat_id": chat_id})
        if not game:
            return None
        if game["expires_at"] < datetime.utcnow():
            await self.clear_active_character(chat_id)
            return None
        return Character(**game["character"])
    
    async def mark_as_guessed(self, chat_id: int, user_id: int) -> bool:
        result = await self.active_games.update_one(
            {"chat_id": chat_id, "guessed_by": None},
            {"$set": {"guessed_by": user_id}}
        )
        return result.modified_count > 0
        async def clear_active_character(self, chat_id: int):
        await self.active_games.delete_one({"chat_id": chat_id})
    
    # === Group Operations ===
    async def get_group_settings(self, chat_id: int) -> Optional[GroupSettings]:
        doc = await self.groups.find_one({"chat_id": chat_id})
        return GroupSettings(**doc) if doc else None
    
    async def increment_message_count(self, chat_id: int) -> int:
        result = await self.groups.find_one_and_update(
            {"chat_id": chat_id},
            {"$inc": {"message_count": 1}, "$setOnInsert": {"message_count": 0}},
            upsert=True,
            return_document=True
        )
        return result.get("message_count", 1)
    
    async def reset_message_count(self, chat_id: int):
        await self.groups.update_one({"chat_id": chat_id}, {"$set": {"message_count": 0}})
    
    # === Trade Operations ===
    async def create_trade(self, trade: TradeOffer) -> bool:
        try:
            await self.trades.insert_one(trade.model_dump())
            return True
        except Exception as e:
            logger.error(f"Failed to create trade: {e}")
            return False
    
    async def get_trade(self, trade_id: str) -> Optional[TradeOffer]:
        doc = await self.trades.find_one({"trade_id": trade_id})
        return TradeOffer(**doc) if doc else None
    
    async def update_trade_status(self, trade_id: str, status: str) -> bool:
        result = await self.trades.update_one(
            {"trade_id": trade_id},
            {"$set": {"status": status}}
        )
        return result.modified_count > 0
