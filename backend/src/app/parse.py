import requests
import json
import time
from datetime import datetime
import os
import threading


def setValueInList(l, i, v):
    l[i] = v


def multithreadExec(funcs: list):
    results = [None] * len(funcs)
    threads = []
    for i in range(len(funcs)):
        threads.append(
            threading.Thread(
                target=lambda: setValueInList(results, i, funcs[i][0](*funcs[i][1]))
            )
        )
        threads[-1].start()

    for thread in threads:
        thread.join()
    return results


def getGeoData(latitude: str, longitude: str):
    print(latitude)
    print(longitude)
    return json.loads(
        requests.get(
            f"https://user-geo-data.wildberries.ru/get-geo-info?currency=RUB&latitude={latitude}&longitude={longitude}&locale=ru"
        ).text
    )


def getProductDelivery(article: str, dest: str):
    return json.loads(
        requests.get(
            f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest={dest}&spp=30&ab_testing=false&nm={article}"
        ).text
    )


def getProductDataByArticle(article: str):
    length = len(article)
    full_article = "0" * (9 - length) + article

    results = []
    threads_count = os.cpu_count()
    steps = [threads_count for i in range(20 // threads_count)]
    steps.append(20 % threads_count)
    for step in steps:
        results.extend(
            multithreadExec(
                [
                    [
                        requests.get,
                        [
                            f"https://basket-{('0' + str(i)) if (i < 10) else str(i)}.wbbasket.ru/vol{str(int(full_article[ : 4]))}/part{str(int(full_article[ : 6]))}/{article}/info/ru/card.json"
                        ],
                    ]
                    for i in range(1 + len(results), 1 + len(results) + step)
                ]
            )
        )
    for result in results:
        if result.status_code == 200:
            return json.loads(result.text)
    return None


def findTitleImageUrlByArticle(article: str):
    length = len(article)
    full_article = "0" * (9 - length) + article

    results = []
    threads_count = os.cpu_count()
    steps = [threads_count for i in range(20 // threads_count)]
    steps.append(20 % threads_count)
    for step in steps:
        results.extend(
            multithreadExec(
                [
                    [
                        requests.get,
                        [
                            f"https://basket-{('0' + str(i)) if (i < 10) else str(i)}.wbbasket.ru/vol{str(int(full_article[ : 4]))}/part{str(int(full_article[ : 6]))}/{article}/images/big/1.webp"
                        ],
                    ]
                    for i in range(1 + len(results), 1 + len(results) + step)
                ]
            )
        )
    for result in results:
        if result.status_code == 200:
            return result.url
    return None


def getProductsByQuery_json(query: str):
    return json.loads(
        requests.get(
            f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
        ).text
    )


def getProductData(article: str, latitude: str, longitude: str):
    data = multithreadExec(
        [
            [getProductDataByArticle, [article]],
            [getProductsByQuery_json, ["товар " + article]],
            [getGeoData, [latitude, longitude]],
            [findTitleImageUrlByArticle, [article]],
        ]
    )

    product_data = data[0]
    product_in_search = data[1]["data"]["products"][0]

    geo_data = data[2]
    dest_i = geo_data["xinfo"].find("dest=") + 5
    nearest_dest = geo_data["xinfo"][dest_i : geo_data["xinfo"].find("&", dest_i)]

    product_delivery_hours = getProductDelivery(article, nearest_dest)["data"][
        "products"
    ][0]["time2"]
    return [
        {
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
                [
                    [option["name"], option["value"]]
                    for option in product_data["options"]
                ]
            ),
        },
        {"images": [data[3]]},
    ]


def getFormatedProductsByQuery(
    query: str, latitude: str, longitude: str, max_count: int
):
    products_data = getProductsByQuery_json(query)["data"]["products"][:max_count]
    products = []
    threads_count = os.cpu_count()
    steps = [threads_count for i in range(len(products_data) // threads_count)]
    steps.append(len(products_data) % threads_count)
    for step in steps:
        products.extend(
            multithreadExec(
                [
                    [getProductData, [str(products_data[j]["id"]), latitude, longitude]]
                    for j in range(len(products), len(products) + step)
                ]
            )
        )
    return products


def getProductsArticlesByQuery(query: str, max_count: int = 1000):
    products_data = getProductsByQuery_json(query)["data"]["products"][:max_count]
    return [product["id"] for product in products_data]


if __name__ == "__main__":
    print("start")
    query = "фен"  # input("text: ")
    art = "48334378"
    # print(getGeoData("55.309228", "82.730587"))
    # print(getProductDelivery(art, "-7165699"))
    # print(getProductDataByArticle("149100663"))
    # print(type(getProductDataByArticle__old("149100663")))
    # print(getFormatedProductsByQuery(query, "55.309228", "82.730587", 10))
    # print(getFormatedProductsByQueryTh(query, "55.309228", "82.730587"))
    print(getProductData("48334378", "55.309228", "82.730587"))

    curr_time = time.time()
    # print(getFormatedProductsByQuery(query, "55.309228", "82.730587", 20))
    print(time.time() - curr_time)
    curr_time = time.time()
    print(getProductsArticlesByQuery(query, "55.309228", "82.730587", 10))
    print(time.time() - curr_time)

    print("end")
