from datetime import date
from typing import Any

import requests
import json
from pydantic import HttpUrl

from app.db.models import Article, Catalog
from app.db.models.catalog import Product
from app.ollama.requests import product_validation


def get_product_data_by_article(article: str) -> Article:
    length = len(article)
    return Article.model_validate_json(
        requests.get(
            f"https://basket-{('0' + article[ : 1]) if (length == 8) else article[ : 2]}.wbbasket.ru/vol{article[ : 3] if (length == 8) else article[ : 5]}/part{article[ : 5] if (length == 8) else article[ : 6]}/{article}/info/ru/card.json"
        ).text
    )


def get_products_by_query(query: str) -> Catalog:
    return Catalog.model_validate_json(
        requests.get(
            f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
        ).text
    )


def generate_optimal_query(article: Any) -> str:
    return product_validation(str(article))


def sort_products_by_ollama(products: list[Product]) -> list[int]:
    # можно вернуть отсортированные продукты list[Product], но в этом особого смысла нет
    articles = [p.id for p in products]
    return articles


def calculate_price(article: Article) -> float:
    return 99.99


def calculate_delivery_date(article: Article) -> date:
    return date.today()


def calculate_rating(article: Article) -> float:
    return 4.5


def calculate_reviews_count(article: Article) -> int:
    return 100


def get_image_urls(article: Article) -> list[HttpUrl]:
    return [
        HttpUrl(f"https://example.com/image_{i}.jpg")
        for i in range(article.media.photo_count)
    ]
