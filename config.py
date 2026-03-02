"""
Central Configuration - Private Repo Safe
All credentials here. NO .env needed.
"""

# === TELEGRAM API ===
BOT_TOKEN = "8424950811:AAE-Jf6wfsPDjsu7J-iqPHlPCDEkq61UXH4"
API_ID = 36455116
API_HASH = "ddbbb57121805c7b1434734390ff2e08"
OWNER_ID = 8327837344
SUDO_USERS = [8327837344]  # Tumhara ID hi sudo hai abhi

# === DATABASE ===
MONGODB_URL = "mongodb+srv://usrhtffdbr:miku1234@cluster0.jhvwttf.mongodb.net/?appName=Cluster0"
REDIS_URL = None  # Redis abhi nahi chahiye, None rehne do
DB_NAME = "AnimeUltimatePro"

# === BOT SETTINGS ===
BOT_USERNAME = "the_mahibot"  # Without @
SUPPORT_CHAT = "the_mahibot"  # Abhi bot hi support hai, baad mein change karna
UPDATE_CHAT = "the_mahibot"   # Abhi bot hi updates hai, baad mein change karna
LOG_LEVEL = "INFO"

# === GAME SETTINGS ===
MESSAGE_THRESHOLD = 100  # 100 messages baad character spawn hoga
SPAM_WINDOW_SECONDS = 600
MAX_GUESSES_PER_USER = 3
GUESS_COOLDOWN = 5  # Seconds between guesses

# === RARITY SYSTEM ===
RARITY_WEIGHTS = {
    "common": 70.0,      # ⚪️ 70% chance
    "medium": 20.0,      # 🟢 20% chance
    "rare": 8.0,         # 🟣 8% chance
    "legendary": 1.5,    # 🟡 1.5% chance
    "mythical": 0.5      # 🔴 0.5% chance
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
    "https://telegra.ph/file/8c27d4c8e6f4e7f8c9d1a.jpg",
    "https://telegra.ph/file/9d38e5d9f7g5f8g9e2b.jpg"
]

# === FEATURE FLAGS ===
ENABLE_TRADING = True
ENABLE_GACHA = True
ENABLE_EVENTS = True
ENABLE_EVOLUTION = True
ENABLE_ANALYTICS = True
