import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "charset": os.getenv("DB_CHARSET"),
}

API_TOKEN=os.getenv("TELEGRAM_TOKEN")