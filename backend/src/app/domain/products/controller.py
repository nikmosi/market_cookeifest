from litestar import Controller, get

from app.db.models import Article, Catalog
from app.domain.products import urls
from app.domain.products.services import (
    get_product_data_by_article,
    get_products_by_query,
)


class ProductsController(Controller):
    tags = ["Products"]

    @get(path=urls.PRODUCT_ID, name="product:get_by_article")
    async def get_product_by_article(self, product_article: str) -> Article:
        return get_product_data_by_article(product_article)

    @get(path=urls.SIMILAR_PRODUCT, name="product:similar")
    async def get_similar_products(self, product_article: str) -> Catalog:
        article = get_product_data_by_article(product_article)
        return get_products_by_query(article.imt_name)
