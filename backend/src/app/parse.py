import asyncio
import time
from datetime import datetime

import httpx
from loguru import logger


async def getGeoData(latitude: str, longitude: str):
    logger.debug(latitude)
    logger.debug(longitude)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://user-geo-data.wildberries.ru/get-geo-info?currency=RUB&latitude={latitude}&longitude={longitude}&locale=ru"
        )
    logger.debug(response.text)
    return response.json()


async def getProductDelivery(article: str, dest: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest={dest}&spp=30&ab_testing=false&nm={article}"
        )
    return response.json()


async def getProductDataByArticle(article: str):
    length = len(article)
    full_article = "0" * (9 - length) + article

    async with httpx.AsyncClient() as client:
        for i in range(1, 21):
            url = f"https://basket-{('0' + str(i)) if i < 10 else str(i)}.wbbasket.ru/vol{str(int(full_article[:4]))}/part{str(int(full_article[:6]))}/{article}/info/ru/card.json"
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
    return None


async def findTitleImageUrlByArticle(article: str):
    length = len(article)
    full_article = "0" * (9 - length) + article

    async with httpx.AsyncClient() as client:
        for i in range(1, 21):
            url = f"https://basket-{('0' + str(i)) if i < 10 else str(i)}.wbbasket.ru/vol{str(int(full_article[:4]))}/part{str(int(full_article[:6]))}/{article}/images/big/1.webp"
            response = await client.get(url)
            if response.status_code == 200:
                return str(response.url)
    return None


async def getProductsByQuery_json(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
        )
    return response.json()


async def getProductData(article: str, latitude: str, longitude: str):
    product_data = await getProductDataByArticle(article)
    search_data = await getProductsByQuery_json("артикул " + article)
    geo_data = await getGeoData(latitude, longitude)
    title_image_url = await findTitleImageUrlByArticle(article)

    if not product_data or not search_data or not geo_data or not title_image_url:
        return None

    product_in_search = search_data["data"]["products"][0]

    dest_i = geo_data["xinfo"].find("dest=") + 5
    nearest_dest = geo_data["xinfo"][dest_i : geo_data["xinfo"].find("&", dest_i)]

    product_delivery = await getProductDelivery(article, nearest_dest)
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


async def getFormatedProductsByQuery(
    query: str, latitude: str, longitude: str, max_count: int
):
    products_data = (await getProductsByQuery_json(query))["data"]["products"][
        :max_count
    ]
    tasks = [
        getProductData(str(product["id"]), latitude, longitude)
        for product in products_data
    ]
    products = await asyncio.gather(*tasks)
    return [product for product in products if product]


async def getProductsArticlesByQuery(query: str, max_count: int = 1000):
    ans = await getProductsByQuery_json(query)
    logger.debug(f"{ans=}")
    logger.debug(f"{query=}")
    products_data = ans["data"]["products"][:max_count]
    return [product["id"] for product in products_data]


# Example Usage:
# asyncio.run(getFormatedProductsByQuery("query", "55.7558", "37.6173", 10))
