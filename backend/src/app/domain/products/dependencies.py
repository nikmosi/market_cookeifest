from httpx import AsyncClient
from litestar import Request
from loguru import logger

from app.domain.products.services import GeoService


async def provide_ip(request: Request) -> str:
    header = request.headers.get("x-forwarded-for")
    logger.debug(f"{header=}")
    ip = None
    if header:
        ip = header.split(",")[0]
    if not ip:
        ip = "127.0.0.1"
    return ip


async def provide_geo_service(client: AsyncClient) -> GeoService:
    return GeoService(client)
