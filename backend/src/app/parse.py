import asyncio
import time
from asyncio import TaskGroup
from datetime import datetime

import httpx
from loguru import logger

from app.alib.exceptions import BasketError
from app.db.models.geo import Geo
from app.db.models.wb import ProductData, WbArticle, WbDelivery, WbGeo, WbProduct
from app.utils.http import fetch_url

BASE_URLS = {
    "geo": "https://user-geo-data.wildberries.ru/get-geo-info?currency=RUB&latitude={latitude}&longitude={longitude}&locale=ru",
    "product_delivery": "https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest={dest}&spp=30&ab_testing=false&nm={article}",
    "basket": "https://basket-{i:02}.wbbasket.ru/vol{full_article_1}/part{full_article_2}/{article}/{postfix}",
    "search": "https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false",
}


async def get_geo_data(geo: Geo) -> WbGeo:
    async with httpx.AsyncClient() as client:
        url = BASE_URLS["geo"].format(latitude=geo.latitude, longitude=geo.longitude)
        response = await fetch_url(client, url)
    return WbGeo.model_validate_json(response.text)


async def get_product_delivery(article: str, dest: str) -> WbDelivery:
    async with httpx.AsyncClient() as client:
        url = BASE_URLS["product_delivery"].format(dest=dest, article=article)
        response = await fetch_url(client, url)
    return WbDelivery.model_validate_json(response.text)


async def generate_urls(article: str, postfix: str) -> list[str]:
    full_article = article.rjust(9, "0")
    logger.debug(BASE_URLS)
    return [
        BASE_URLS["basket"].format(
            i=i,
            full_article_1=full_article[:4].lstrip("0"),
            full_article_2=full_article[:6].lstrip("0"),
            article=article,
            postfix=postfix,
        )
        for i in range(1, 21)
    ]


async def helper_basket(
    article: str, postfix: str, timeout: float = 10.0
) -> httpx.Response:
    urls = await generate_urls(article, postfix)
    result = None

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout)) as client:
        tasks = [asyncio.create_task(fetch_url(client, url)) for url in urls]
        logger.info("Starting basket requests")

        for coro in asyncio.as_completed(tasks):
            response = await coro
            if response and response.status_code == 200:
                logger.info(f"Successful response from {response.url}")
                result = response
                break

        for task in tasks:
            if not task.done():
                task.cancel()

        if result:
            return result

    logger.warning("No successful responses")
    raise BasketError(article, postfix)


async def get_product_data_by_article(article: str) -> WbArticle:
    res = await helper_basket(article, "info/ru/card.json")
    return WbArticle.model_validate_json(res.text)


async def find_title_image_url_by_article(article: str) -> str:
    res = await helper_basket(article, "images/big/1.webp")
    return str(res.url)


async def get_products_by_query_json(query: str) -> WbProduct:
    async with httpx.AsyncClient() as client:
        url = BASE_URLS["search"].format(query=query)
        response = await fetch_url(client, url)
    return WbProduct.model_validate_json(response.text)


async def get_product_data(article: str, geo: Geo) -> ProductData | None:
    async with TaskGroup() as tg:
        wb_article = tg.create_task(get_product_data_by_article(article))
        wb_product = tg.create_task(get_products_by_query_json("артикул " + article))
        geo_data = tg.create_task(get_geo_data(geo))
        image_urls = tg.create_task(find_title_image_url_by_article(article))

    wb_article = await wb_article
    wb_product = await wb_product
    geo_data = await geo_data
    image_urls = await image_urls

    if not all((wb_article, wb_product, geo_data, image_urls)):
        return None

    product_in_search = wb_product.data.products[0]
    url = httpx.URL(f"http://dummy.com/?{geo_data.xinfo}")
    params = url.params
    nearest_dest = params.get("dest")

    wb_delivery = await get_product_delivery(article, nearest_dest)
    if wb_delivery is None:
        return None

    product_delivery_hours = wb_delivery.data.products[0].time2
    return ProductData(
        **{
            "id": article,
            "name": wb_article.imt_name,
            "description": wb_article.description,
            "price": float(product_in_search.sizes[0].price.total / 100),
            "delivery": datetime.fromtimestamp(
                time.time() + product_delivery_hours * 60 * 60
            ).strftime("%d.%m.%Y"),
            "rating": float(product_in_search.reviewRating),
            "reviews_count": int(product_in_search.feedbacks),
            "options": dict(
                [[option.name, option.value] for option in wb_article.options]
            ),
            "images": [image_urls],
        }
    )


async def get_products_articles_by_query(
    query: str, max_count: int = 1000
) -> list[int]:
    ans = await get_products_by_query_json(query)
    if ans:
        products_data = ans.data.products[:max_count]
        articles = [product.id for product in products_data]
        return articles
    return []
