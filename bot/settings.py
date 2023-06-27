from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DB_URL')
    token: str = Field(..., env='TOKEN')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings(_env_file=".env")
