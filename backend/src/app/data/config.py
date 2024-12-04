from pydantic import BaseModel, Field, RedisDsn
from pydantic_settings import BaseSettings


class RedisConfig(BaseModel):
    url: RedisDsn = Field(default=RedisDsn("redis://default:password@redis:6379/0"))


class OllamaConfig(BaseModel):
    host: str = "ollama:11434"
    model: str = "llama3.1"


class Config(BaseSettings):
    redis: RedisConfig = RedisConfig()
    ollama: OllamaConfig = OllamaConfig()


config = Config()
