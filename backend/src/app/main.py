from litestar import Litestar, get
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


app = create_app()
