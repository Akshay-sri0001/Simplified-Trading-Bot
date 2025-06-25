# config.py
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
API_SECRET = os.getenv("BINANCE_TESTNET_API_SECRET")

FUTURES_TESTNET_URL = "https://testnet.binancefuture.com"

if not API_KEY or not API_SECRET:
    raise ValueError("API_KEY and API_SECRET must be set in .env file or environment variables.")