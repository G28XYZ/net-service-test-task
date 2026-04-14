import os
import re

from dotenv import load_dotenv


load_dotenv()


class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/vm_service",
    )

    @property
    def async_database_url(self) -> str:
        return re.sub(r"^postgresql:", "postgresql+psycopg:", self.database_url)


settings = Settings()

