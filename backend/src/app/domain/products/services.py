import json

import requests

from app.db.models import Article, Catalog


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
