import os
from ollama import Client

host = os.getenv("OLLAMA_HOST")

client = Client(host=host, headers={"x-some-header": "some-value"})
print(host)
