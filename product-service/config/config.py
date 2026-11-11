import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL


SERVICE_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(SERVICE_ROOT / ".env")


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    REDIS_URL = os.environ["REDIS_URL"]

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False