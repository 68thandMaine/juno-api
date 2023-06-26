import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    def __init__(self):
        db_username: str = Field(..., env="DATABASE_USERNAME")
        db_password: str = Field(..., env="DATABASE_PASSWORD")
        db_port: str = Field(..., env="DATABASE_PORT")
        db_url: str = Field(..., env="DATABASE_URL")
        db_dialect: str = Field(..., env="DATABASE_DIALECT")

    @property
    def db_connection(self):
        return f"{self.db_dialect}++asyncpg://{self.db_username}:{self.db_password}@{self.db_url}"


settings = Settings()
