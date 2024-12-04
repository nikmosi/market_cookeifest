from typing import Any

from app.db.models.catalog import Product
from app.ollama.requests import product_validation


async def generate_optimal_query(article: Any) -> str:
    return article[0]["name"]
    return await product_validation(article)


def sort_products_by_ollama(products: list[Product]) -> list[int]:
    articles = [p.id for p in products]
    return articles
