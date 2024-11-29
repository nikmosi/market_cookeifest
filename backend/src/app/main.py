from typing import Any

from litestar import Litestar, get

from app.models import WbAns
from app.parse import getProductDataByArticle, getProductsByQuery


@get("/")
async def index() -> str:
    return "Hello, world!"


@get("/catalog/{text:str}")
async def get_catalog_by_query(text: str) -> WbAns:
    return getProductsByQuery(text)


@get("/catalog/{article:str}")
async def get_product_by_article(article: str) -> Any:
    return getProductDataByArticle(article)


def create_app() -> Litestar:
    return Litestar(
        [index, get_catalog_by_query, get_product_by_article],
    )


app = create_app()
