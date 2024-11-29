from typing import Any

from litestar import Litestar, get

from app.routes import route_handlers


@get("/")
async def index() -> str:
    return "Hello, world!"


def create_app() -> Litestar:
    return Litestar(
        route_handlers=route_handlers + [index],
    )


app = create_app()
