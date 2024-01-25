import os
from sys import modules

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    db_username: str = os.getenv("DATABASE_USERNAME", "")
    db_password: str = os.getenv("DATABASE_PASSWORD", "")
    db_port: str = os.getenv("DATABASE_PORT", "")
    db_url: str = os.getenv("DATABASE_URL", "")
    db_dialect: str = os.getenv("DATABASE_DIALECT", "")

    @property
    def db_connection(self):
        """the database connection to the Juno Postgres DB

        Returns:
            str: url string for the db connection
        """

        database = "/juno_db_test" if "pytest" in modules else "/juno_db"
        return f"{self.db_dialect}+asyncpg://{self.db_username}:{self.db_password}@{self.db_url}:{self.db_port}{database}"


settings = Settings()
