import requests
import json
import time
from datetime import datetime

from app.models import WbAns


def getGeoData(latitude: str, longitude: str):
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
    return json.loads(
        requests.get(
            f"https://basket-{('0' + article[ : 1]) if (length == 8) else article[ : 2]}.wbbasket.ru/vol{article[ : 3] if (length == 8) else article[ : 5]}/part{article[ : 5] if (length == 8) else article[ : 6]}/{article}/info/ru/card.json"
        ).text
    )


def findTitleImageUrlByArticle(article: str):
    length = len(article)
    for i in range(1, 21):
        req = requests.get(f"https://basket-{('0' + str(i)) if (i < 10) else str(i)}.wbbasket.ru/vol{article[ : 3] if (length == 8) else article[ : 5]}/part{article[ : 5] if (length == 8) else article[ : 6]}/{article}/images/big/1.webp")
        if (req.text.find("DOCTYPE") == -1):
            return req.url
    return None


def getProductsByQuery__new(query: str):
    return json.loads(
        requests.get(
            f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
        ).text
    )


def getProductData(article: str, latitude: str, longitude: str):
    product_data = getProductDataByArticle(article)
    product_in_search = getProductsByQuery__new("товар " + article)["data"]["products"][0]
    
    geo_data = getGeoData(latitude, longitude)
    dest_i = geo_data["xinfo"].find("dest=") + 5
    nearest_dest = geo_data["xinfo"][dest_i : geo_data["xinfo"].find("&", dest_i)]
    
    product_delivery_hours = getProductDelivery(article, nearest_dest)["data"]["products"][0]["time2"]
    return [
        {
            "id": article,
            "name": product_data["imt_name"],
            "description": product_data["description"],
            "price": float(product_in_search["sizes"][0]["price"]["total"]/100),
            "delivery": datetime.fromtimestamp(time.time() + product_delivery_hours*60*60).strftime("%d.%m.%Y"),
            "rating": float(product_in_search["reviewRating"]),
            "reviews_count": int(product_in_search["feedbacks"]),
            "options": dict([[option["name"], option["value"]] for option in product_data["options"]])
        },
        {"images": [findTitleImageUrlByArticle(article)]}
    ]


def getProductsByQuery(query: str) -> WbAns:
    return WbAns.model_validate_json(
        requests.get(
            f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
        ).text
    )


if __name__ == "__main__":
    query = "фен"  # input("text: ")
    art = "48334378"
    #print(getGeoData("55.309228", "82.730587"))
    print(getProductDelivery(art, "-7165699"))
    #print(getProductDataByArticle(art))
    #print(getProductsByQuery("товар " + query))
    print(getProductData("48334378", "55.309228", "82.730587"))
    print("end")
