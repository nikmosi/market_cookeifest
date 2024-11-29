from ollama import Client

from ollama import chat
from ollama import ChatResponse

client = Client(
    host="http://ollama_mklp.serveo.net", headers={"x-some-header": "some-value"}
)
stream = client.chat(
    model="llama3.1",
    messages=[{"role": "user", "content": "Write snake on python"}],
    stream=True,
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
