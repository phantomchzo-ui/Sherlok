import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = int(os.getenv("DB_PORT", 5432))
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")

        self.TOKEN = os.getenv("TOKEN")

        # Проверки (очень желательно)
        self._validate()

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    def _validate(self):
        if not self.TOKEN:
            raise ValueError("TOKEN не задан")
        if not self.DB_HOST:
            raise ValueError("DB_HOST не задан")


# создаём экземпляр
settings = Settings()