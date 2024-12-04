from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from litestar.config.response_cache import ResponseCacheConfig
from litestar.stores.redis import RedisStore

from app.routes import route_handlers


@get("/health", tags=["hidden"])
async def index() -> str:
    return "Hello, world!"


def create_app() -> Litestar:
    cors_config = CORSConfig(allow_origins=["*"])
    redis_store = RedisStore.with_client(
        url="redis://redis/", port=6379, db=0, username="default", password="password"
    )
    cache_config = ResponseCacheConfig(store="redis_backed_store")
    return Litestar(
        route_handlers=route_handlers + [index],
        stores={"redis_backed_store": redis_store},
        response_cache_config=cache_config,
        cors_config=cors_config,
    )


app = create_app()
