from sqlalchemy import create_engine
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url:str

    class Config:
        env_file=".env"
        env_file_encoding="utf-8"

settings= Settings()

engine =create_engine(settings.database_url , echo=True)
