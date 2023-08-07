import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_username: str = os.getenv("DATABASE_USERNAME") or "postgres"
    db_password: str = os.getenv("DATABASE_PASSWORD") or "postgres"
    db_port: str = os.getenv("DATABASE_PORT") or 5432
    db_url: str = os.getenv("DATABASE_URL") or "postgres"
    db_dialect: str = os.getenv("DATABASE_DIALECT") or "postgresql"

    @property
    def db_connection(self):
        """the database connection to the Juno Postgres DB

        Returns:
            str: url string for the db connection
        """

        return f"{self.db_dialect}+asyncpg://{self.db_username}:{self.db_password}@{self.db_url}:{self.db_port}"


settings = Settings()
