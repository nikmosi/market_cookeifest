from litestar import Litestar, get
from ollama import Client

from ollama import chat
from ollama import ChatResponse
from app.models import WbAns
from app.parse import getProductsByQuery


@get("/")
async def index() -> str:
    return "Hello, world!"


@get("/catalog/{text:str}")
async def get_catalog_by_query(text: str) -> WbAns:
    return getProductsByQuery(text)


def create_app() -> Litestar:
    return Litestar(
        [index, get_catalog_by_query],
    )


client = Client(
    host="http://ollama_mklp.serveo.net", headers={"x-some-header": "some-value"}
)
stream = client.chat(
    model="llama3.1",
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
    stream=True,
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)

app = create_app()
