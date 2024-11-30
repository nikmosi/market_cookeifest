from litestar import Litestar, Request, get
from litestar.config.response_cache import ResponseCacheConfig
from litestar.stores.redis import RedisStore

from app.routes import route_handlers


@get("/")
async def index() -> str:
    return "Hello, world!"


@get("/ip")
async def get_ip(request: Request) -> str:
    client_ip = request.scope.get("client", ["Unknown"])
    return f"Your IP address is: {client_ip}"


def create_app() -> Litestar:
    redis_store = RedisStore.with_client(
        url="redis://redis/", port=6379, db=0, username="default", password="password"
    )
    cache_config = ResponseCacheConfig(store="redis_backed_store")
    return Litestar(
        route_handlers=route_handlers + [index, get_ip],
        stores={"redis_backed_store": redis_store},
        response_cache_config=cache_config,
    )


app = create_app()
