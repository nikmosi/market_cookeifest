from litestar import Controller, get

from app.db.models import Article
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
    async def get_product_by_article(self, product_article: str) -> Article:
        return get_product_data_by_article(product_article)

    @get(path=urls.SIMILAR_PRODUCT, name="product:similar")
    async def get_similar_products(self, product_article: str) -> SimilarProducts:
        article = get_product_data_by_article(product_article)
        query = generate_optimal_query(article)
        catalog = get_products_by_query(query)
        products = catalog.data.products
        articles = sort_products_by_ollama(products)
        return SimilarProducts(articles=articles)
