from typing import Any

import httpx
from litestar import Controller, Request, get
from loguru import logger

from app.domain.products import urls
from app.domain.products.schemas import SimilarProducts
from app.domain.products.services import (
    generate_optimal_query,
)
from app.parse import getProductData, getProductsArticlesByQuery


class ProductsController(Controller):
    tags = ["Products"]

    async def get_ll(self, ip: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://geolocation-db.com/json/{ip}&position=true"
            )
            response_data = response.json()

            if response_data.get("latitude") == "Not found":
                logger.debug(
                    "Can't get location from user IP; defaulting to Novosibirsk"
                )
                response = await client.get(
                    "https://geolocation-db.com/json/37.192.128.147&position=true"
                )
                response_data = response.json()

        return response_data

    async def get_ip(self, request: Request) -> str:
        ip_header = request.headers.get("x-forwarded-for")
        ip = None
        if ip_header:
            ip = ip_header.split(",")[0]
            logger.debug(f"{ip=}")
        if not ip:
            ip = "127.0.0.1"
        return ip

    @get(path=urls.PRODUCT_ID, name="product:get_by_article", cache=360)
    async def get_product_by_article(
        self, product_article: str, request: Request
    ) -> Any:
        ip = await self.get_ip(request)
        geo = await self.get_ll(ip)

        product = await getProductData(
            product_article, geo["latitude"], geo["longitude"]
        )
        logger.debug(f"{product=}")

        return product

    @get(path=urls.SIMILAR_PRODUCT, name="product:similar", cache=360)
    async def get_similar_products(self, request: Request, product_article: str) -> Any:
        ip = await self.get_ip(request)
        geo = await self.get_ll(ip)
        product = await getProductData(
            product_article, geo["latitude"], geo["longitude"]
        )
        query = await generate_optimal_query(product)
        articles = await getProductsArticlesByQuery(query, max_count=20)
        return SimilarProducts(articles=articles)
