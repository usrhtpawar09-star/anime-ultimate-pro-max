"""
Central Configuration - Private Repo Safe
All credentials here. NO .env needed.
"""

# === TELEGRAM API ===
BOT_TOKEN = "123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
API_ID = 1234567
API_HASH = "0123456789abcdef0123456789abcdef"
OWNER_ID = 123456789
SUDO_USERS = [123456789, 987654321]

# === DATABASE ===
MONGODB_URL = "mongodb+srv://user:pass@cluster.mongodb.net/anime_bot?retryWrites=true&w=majority"
REDIS_URL = None  # Set to "redis://localhost:6379/0" if using Redis
DB_NAME = "AnimeUltimatePro"

# === BOT SETTINGS ===
BOT_USERNAME = "YourProBot"
SUPPORT_CHAT = "your_support_group"
UPDATE_CHAT = "your_updates_channel"
LOG_LEVEL = "INFO"

# === GAME SETTINGS ===
MESSAGE_THRESHOLD = 100
SPAM_WINDOW_SECONDS = 600
MAX_GUESSES_PER_USER = 3
GUESS_COOLDOWN = 5

# === RARITY SYSTEM ===
RARITY_WEIGHTS = {
    "common": 70.0,
    "medium": 20.0,
    "rare": 8.0,
    "legendary": 1.5,
    "mythical": 0.5
}

# === ECONOMY ===
REWARD_COINS = {
    "common": 10,
    "medium": 25,
    "rare": 50,
    "legendary": 150,
    "mythical": 500
}
REWARD_GEMS = {
    "common": 0,
    "medium": 0,
    "rare": 1,
    "legendary": 3,
    "mythical": 10
}

# === TRADING ===
TRADE_EXPIRY_MINUTES = 15
TRADE_FEE_PERCENT = 5

# === EVOLUTION ===
EVOLUTION_COST_MULTIPLIER = 3
MIN_EVOLUTION_COPIES = 5

# === EVENTS ===
EVENT_BONUS_MULTIPLIER = 1.5
DEFAULT_PHOTOS = [
    "https://telegra.ph/file/default1.jpg",
    "https://telegra.ph/file/default2.jpg"
]

# === FEATURE FLAGS ===
ENABLE_TRADING = True
ENABLE_GACHA = True
ENABLE_EVENTS = True
ENABLE_EVOLUTION = True
ENABLE_ANALYTICS = True
