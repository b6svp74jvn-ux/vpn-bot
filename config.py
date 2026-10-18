import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
PRICE_RUB = int(os.getenv("PRICE_RUB", "150"))
TRIAL_DAYS = int(os.getenv("TRIAL_DAYS", "3"))
