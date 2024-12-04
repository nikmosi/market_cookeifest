import asyncio
import time
from datetime import datetime

import httpx
from loguru import logger

from app.db.models.geo import Geo
from app.db.models.wb import WbDelivery, WbGeo


async def get_geo_data(geo: Geo) -> WbGeo:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://user-geo-data.wildberries.ru/get-geo-info?currency=RUB&latitude={geo.latitude}&longitude={geo.longitude}&locale=ru"
        )
    return WbGeo.model_validate_json(response.text)


async def get_product_delivery(article: str, dest: str) -> WbDelivery:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest={dest}&spp=30&ab_testing=false&nm={article}"
        )
    logger.debug(f"delivery: {response.text=}")
    return WbDelivery.model_validate_json(response.text)


async def generate_urls(article: str, postfix: str) -> list[str]:
    full_article = article.rjust(9, "0")
    return [
        f"https://basket-{i:02}.wbbasket.ru/vol{full_article[:4]}/part{full_article[:6]}/{article}/{postfix}"
        for i in range(1, 21)
    ]


async def helper_basket(article: str, postfix: str, timeout: float = 10.0):
    urls = await generate_urls(article, postfix)

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout)) as client:
        tasks = [client.get(url) for url in urls]
        logger.info("Starting basket requests")

        for coro in asyncio.as_completed(tasks):
            try:
                response = await coro
                if response.status_code == 200:
                    logger.info(f"Successful response from {response.url}")
                    return response
            except httpx.RequestError as e:
                logger.error(f"Request failed: {e}")

    logger.warning("No successful responses")
    return None


async def get_product_data_by_article(article: str):
    res = await helper_basket(article, "info/ru/card.json")
    return res.json()


async def find_title_image_url_by_article(article: str):
    res = await helper_basket(article, "images/big/1.webp")
    return str(res.url)


async def get_products_by_query_json(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
        )
    json = response.json()
    logger.debug(f"get_products_by_query_json: {json=}")
    return json


async def get_product_data(article: str, geo: Geo):
    product_data = await get_product_data_by_article(article)
    search_data = await get_products_by_query_json("артикул " + article)
    geo_data = await get_geo_data(geo)
    title_image_url = await find_title_image_url_by_article(article)

    if not all((product_data, search_data, geo_data, title_image_url)):
        return None

    product_in_search = search_data["data"]["products"][0]

    nearest_dest = httpx.URL(geo_data.xinfo).params.get("dest")

    product_delivery = await get_product_delivery(article, nearest_dest)
    product_delivery_hours = product_delivery.data.products[0].time2

    return {
        "id": article,
        "name": product_data["imt_name"],
        "description": product_data["description"],
        "price": float(product_in_search["sizes"][0]["price"]["total"] / 100),
        "delivery": datetime.fromtimestamp(
            time.time() + product_delivery_hours * 60 * 60
        ).strftime("%d.%m.%Y"),
        "rating": float(product_in_search["reviewRating"]),
        "reviews_count": int(product_in_search["feedbacks"]),
        "options": dict(
            [[option["name"], option["value"]] for option in product_data["options"]]
        ),
        "images": [title_image_url],
    }


async def get_products_articles_by_query(query: str, max_count: int = 1000):
    ans = await get_products_by_query_json(query)
    logger.debug(f"{ans=}")
    logger.debug(f"{query=}")
    products_data = ans["data"]["products"][:max_count]
    return [product["id"] for product in products_data]


# Example Usage:
# asyncio.run(getFormatedProductsByQuery("query", "55.7558", "37.6173", 10))
