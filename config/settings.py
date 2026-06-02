from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    provider: Literal["ollama", "openai"] = "ollama"
    
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "llama3" # gpt-4o-mini
    openai_api_key: str = ""

    rabbitmq_url: str = "pyamqp://guest:guest@localhost:5672//"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()