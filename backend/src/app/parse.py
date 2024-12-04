import asyncio
import time
from datetime import datetime

import httpx
from loguru import logger


async def get_geo_data(latitude: float, longitude: float):
    logger.debug(latitude)
    logger.debug(longitude)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://user-geo-data.wildberries.ru/get-geo-info?currency=RUB&latitude={latitude}&longitude={longitude}&locale=ru"
        )
    json = response.json()
    logger.debug(f"geo_data: {json=}")
    return json


async def get_product_delivery(article: str, dest: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest={dest}&spp=30&ab_testing=false&nm={article}"
        )
    json = response.json()
    logger.debug(f"delivety: {json=}")
    return json


async def helper_basket(article: str, postfix: str):
    length = len(article)
    full_article = "0" * (9 - length) + article

    async with httpx.AsyncClient() as client:
        reqs = []
        logger.warning("new basket")
        for i in range(1, 21):
            url = f"https://basket-{i:02}.wbbasket.ru/vol{full_article[:4]}/part{full_article[:6]}/{article}/{postfix}"
            reqs.append(asyncio.create_task(client.get(url)))
        done, pending = await asyncio.wait(reqs, return_when=asyncio.FIRST_COMPLETED)
        while pending:
            done, pending = await asyncio.wait(
                reqs, return_when=asyncio.FIRST_COMPLETED
            )
            for req in done:
                response = await req
                if response.status_code == 200:
                    for i in pending:
                        i.cancel()
                    return response
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


async def get_product_data(article: str, latitude: float, longitude: float):
    product_data = await get_product_data_by_article(article)
    search_data = await get_products_by_query_json("артикул " + article)
    geo_data = await get_geo_data(latitude, longitude)
    title_image_url = await find_title_image_url_by_article(article)

    if not product_data or not search_data or not geo_data or not title_image_url:
        return None

    product_in_search = search_data["data"]["products"][0]

    dest_i = geo_data["xinfo"].find("dest=") + 5
    nearest_dest = geo_data["xinfo"][dest_i : geo_data["xinfo"].find("&", dest_i)]

    product_delivery = await get_product_delivery(article, nearest_dest)
    product_delivery_hours = product_delivery["data"]["products"][0]["time2"]

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
