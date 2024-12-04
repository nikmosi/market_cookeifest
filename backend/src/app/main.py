from collections.abc import AsyncGenerator

import httpx
from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from litestar.config.response_cache import ResponseCacheConfig
from litestar.di import Provide
from litestar.stores.redis import RedisStore
from redis.asyncio import ConnectionPool, Redis

from app.data import config
from app.routes import route_handlers


@get("/health", tags=["inside"])
async def index() -> str:
    return "Hello, world!"


async def provide_client() -> AsyncGenerator[httpx.AsyncClient]:
    async with httpx.AsyncClient() as client:
        yield client


def create_app() -> Litestar:
    cors_config = CORSConfig(allow_origins=["*"])
    redis_store = RedisStore(
        Redis(connection_pool=ConnectionPool.from_url(f"{config.redis.url}"))
    )
    cache_config = ResponseCacheConfig(store="redis_backed_store")
    return Litestar(
        route_handlers=route_handlers + [index],
        stores={"redis_backed_store": redis_store},
        response_cache_config=cache_config,
        cors_config=cors_config,
        dependencies={"client": Provide(provide_client)},
    )


app = create_app()
