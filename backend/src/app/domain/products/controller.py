from typing import Any

from litestar import Controller, get
from litestar.di import Provide
from loguru import logger

from app.domain.products import urls
from app.domain.products.schemas import SimilarProducts
from app.domain.products.services import (
    GeoService,
    generate_optimal_query,
)
from app.parse import get_product_data, get_products_articles_by_query

from .dependencies import provide_geo_service, provide_ip


class ProductsController(Controller):
    tags = ["Products"]

    dependencies = {
        "ip": Provide(provide_ip),
        "geo_service": Provide(provide_geo_service),
    }

    @get(path="/api/get_ip", name="product:get_ip", cache=False)
    async def get_ip(self, ip: str) -> Any:
        return {"ip": ip}

    @get(path=urls.PRODUCT_ID, name="product:get_by_article", cache=360)
    async def get_product_by_article(
        self, ip: str, geo_service: GeoService, product_article: str
    ) -> Any:
        geo = await geo_service.get_geo(ip)
        product = await get_product_data(product_article, geo)
        logger.debug(f"{product=}")
        return product

    @get(path=urls.SIMILAR_PRODUCT, name="product:similar", cache=360)
    async def get_similar_products(
        self, ip: str, geo_service: GeoService, product_article: str
    ) -> Any:
        geo = await geo_service.get_geo(ip)
        product = await get_product_data(product_article, geo)
        query = await generate_optimal_query(product)
        articles = await get_products_articles_by_query(query, max_count=20)
        return SimilarProducts(articles=articles)
