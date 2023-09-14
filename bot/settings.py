from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = Field(..., env="DB_URL")
    token: str = Field(..., env="TOKEN")
    admin_id: str = Field(..., env="ADMIN_ID")
    super_admin: str = Field(..., env="SUPER_ADMIN")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings(_env_file=".env")
