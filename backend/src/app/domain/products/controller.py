from litestar import Controller, Request, get
from typing import Any

from app.parse import getGeoData, getProductData
import requests
from app.domain.products import urls
from app.domain.products.schemas import SimilarProducts
from app.domain.products.services import (
    generate_optimal_query,
    get_product_data_by_article,
    get_products_by_query,
    sort_products_by_ollama,
)


class ProductsController(Controller):
    tags = ["Products"]

    @get(path=urls.PRODUCT_ID, name="product:get_by_article")
    async def get_product_by_article(
        self, product_article: str, request: Request
    ) -> Any:
        ip = request.scope.get("client", ["Unknown"])[0]
        response = requests.get(
            f"https://geolocation-db.com/json/{ip}&position=true"
        ).json()
        return getProductData(
            product_article, response["latitude"], response["longitude"]
        )

    @get(path=urls.SIMILAR_PRODUCT, name="product:similar")
    async def get_similar_products(self, request: Request, product_article: str) -> Any:
        ip = request.scope.get("client", ["Unknown"])[0]
        response = requests.get(
            f"https://geolocation-db.com/json/{ip}&position=true"
        ).json()
        article = getProductData(
            product_article, response["latitude"], response["longitude"]
        )
        query = generate_optimal_query(article)
        catalog = get_products_by_query(query)
        products = catalog.data.products
        articles = sort_products_by_ollama(products)
        return SimilarProducts(articles=articles)
