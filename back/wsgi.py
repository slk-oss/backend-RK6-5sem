from config.app import AppConfig
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host=AppConfig.AppHost,
        port=int(AppConfig.AppPort),
        debug=True
    )