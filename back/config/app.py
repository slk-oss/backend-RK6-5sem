import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
    AppPort = os.getenv("APP_PORT")
    AppHost = os.getenv("APP_HOST")