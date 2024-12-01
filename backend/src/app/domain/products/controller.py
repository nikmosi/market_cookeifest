from json import JSONDecodeError
from typing import Any

import requests
from litestar import Controller, Request, get

from app.domain.products import urls
from app.domain.products.schemas import SimilarProducts
from app.domain.products.services import (
    generate_optimal_query,
    get_product_data_by_article,
    get_products_by_query,
    sort_products_by_ollama,
)

# from app.parse import getGeoData, getProductData
from app.parse import getProductData, getProductsArticlesByQuery


class ProductsController(Controller):
    tags = ["Products"]

    @get(path=urls.PRODUCT_ID, name="product:get_by_article", cache=360)
    async def get_product_by_article(
        self, product_article: str, request: Request
    ) -> Any:
        ip = request.headers.get("x-forwarded-for").split(",")[0]
        print(ip)
        response = requests.get(
            f"https://geolocation-db.com/json/{ip}&position=true"
        ).json()
        if response["latitude"] == "Not found":
            print("can't get ip from user ip get from novosibirk")
            response = requests.get(
                f"https://geolocation-db.com/json/37.192.128.147&position=true"
            ).json()
        product = getProductData(
            product_article, response["latitude"], response["longitude"]
        )
        print(product)

        return product

    @get(path=urls.SIMILAR_PRODUCT, name="product:similar", cache=360)
    async def get_similar_products(self, request: Request, product_article: str) -> Any:
        ip = request.headers.get("x-forwarded-for").split(",")[0]
        print(ip)
        response = requests.get(
            f"https://geolocation-db.com/json/{ip}&position=true"
        ).json()
        if response["latitude"] == "Not found":
            print("can't get ip from user ip get from novosibirk")
            response = requests.get(
                f"https://geolocation-db.com/json/37.192.128.147&position=true"
            ).json()
        product = getProductData(
            product_article, response["latitude"], response["longitude"]
        )
        query = generate_optimal_query(product)
        articles = getProductsArticlesByQuery(query, max_count=20)
        return SimilarProducts(articles=articles)
