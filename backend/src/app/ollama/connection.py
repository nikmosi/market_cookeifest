from ollama import AsyncClient

from app.data import config

client = AsyncClient(host=config.ollama.host)
