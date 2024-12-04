import os

from ollama import AsyncClient

host = os.getenv("OLLAMA_HOST")

client = AsyncClient(host=host, headers={"x-some-header": "some-value"})
print(host)
