import os
from dotenv import load_dotenv

load_dotenv()

class PostgresConfig:
    PostgresUser = os.getenv("DB_USER")
    PostgresPassword = os.getenv("DB_PASSWORD")
    DbName = os.getenv("DB_NAME")
    DbHost = os.getenv("DB_HOST")
    DbPort = os.getenv("DB_PORT")

