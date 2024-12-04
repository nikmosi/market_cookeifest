from typing import Any

from httpx import AsyncClient
from loguru import logger
from pydantic import ValidationError

from app.db.models.geo import Geo
from app.ollama.requests import product_validation


class GeoService:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    async def __get(self, ip: str) -> Geo | None:
        response = await self.client.get(
            f"https://geolocation-db.com/json/{ip}&position=true"
        )
        try:
            return Geo.model_validate_json(response.text)
        except ValidationError:
            return None

    async def get_geo(self, ip: str) -> Geo:
        geo = await self.__get(ip)

        if not geo:
            logger.debug("Can't get location from user IP; defaulting to Novosibirsk")

            return Geo.model_validate(
                {
                    "country_code": "RU",
                    "country_name": "Russia",
                    "city": "Novosibirsk",
                    "postal": "630033",
                    "latitude": 55.0411,
                    "longitude": 82.9344,
                    "IPv4": "37.192.128.147",
                    "state": "Novosibirsk Oblast",
                }
            )
        return geo


async def generate_optimal_query(article: Any) -> str:
    logger.debug(article)
    return article["name"]
    return await product_validation(article)
