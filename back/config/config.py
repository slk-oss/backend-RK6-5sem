from config.database import PostgresConfig #RedisConfig
from config.app import AppConfig

class Config(PostgresConfig, AppConfig):
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{PostgresConfig.PostgresUser}:{PostgresConfig.PostgresPassword}"
        f"@{PostgresConfig.DbHost}:{PostgresConfig.DbPort}/{PostgresConfig.DbName}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False