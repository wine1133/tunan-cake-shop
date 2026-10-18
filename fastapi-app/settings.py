import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data"))).expanduser().resolve()
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", str(BASE_DIR / "static" / "uploads"))).expanduser().resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Zero-config default for local development. Set DB_URL to a MySQL URL in production.
DB_URL = os.getenv("DB_URL", "sqlite://data/cake_shop.db")
SECRET_KEY = os.getenv("SECRET_KEY", "tunan-cake-shop-change-this-secret-in-production")
TOKEN_EXPIRE_HOURS = int(os.getenv("TOKEN_EXPIRE_HOURS", "24"))
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173",
    ).split(",")
    if origin.strip()
]