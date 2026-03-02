"""
Redis cache layer (optional - safe if not configured).
"""
import logging
from typing import Optional, Any
from config import REDIS_URL

logger = logging.getLogger(__name__)

class RedisCache:
    """Simple Redis cache wrapper with fallback"""
    
    def __init__(self):
        self.redis = None
        self.default_ttl = 3600
    
    async def connect(self):
        if not REDIS_URL:
            logger.info("⚠️ Redis not configured, skipping")
            return
        try:
            import aioredis
            self.redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
            logger.info("✅ Redis connected")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            self.redis = None
    
    async def get(self, key: str) -> Optional[Any]:
        if not self.redis:
            return None
        try:
            import json
            data = await self.redis.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        if not self.redis:
            return False
        try:
            import json
            ttl = ttl or self.default_ttl
            await self.redis.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        if not self.redis:
            return False
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    async def close(self):
        if self.redis:
            await self.redis.close()

# Global instance
cache = RedisCache()
