import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env relative to this file's location
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    OPENAI_MODEL: str
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()