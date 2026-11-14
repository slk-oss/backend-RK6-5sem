import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL


SERVICE_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(Path(__file__).resolve().parents[1] / ".env.local")


class Config:
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ["SECRET_KEY"]
    REDIS_URL = os.environ["REDIS_URL"]
    PRODUCT_SERVICE_URL = os.environ["PRODUCT_SERVICE_URL"]