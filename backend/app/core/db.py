from sqlalchemy import create_engine
from pydantic_settings import BaseSettings
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

class Settings(BaseSettings):
    database_url:str

    class Config:
        env_file=".env"
        env_file_encoding="utf-8"

settings= Settings()

engine =create_engine(settings.database_url , echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db()-> Generator[Session , None ,None]:
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()
