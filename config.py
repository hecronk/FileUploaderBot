import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

API_BASE = "http://127.0.0.1:8000"
WS_BASE = "ws://127.0.0.1:8000"
FILE_SERVE_BASE = "http://127.0.0.1:8001/"
