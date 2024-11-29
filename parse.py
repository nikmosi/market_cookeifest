import requests
from bs4 import BeautifulSoup
import json
import csv


if (__name__ == "__main__"):
    
    url = "https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query=%D0%BA%D1%80%D0%B5%D0%BC%20%D0%B4%D0%BB%D1%8F%20%D1%80%D1%83%D0%BA&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
    
    req = requests.get(url)
    print(dir(req))
    print(req.text)
    src = req.text
    
    bs = BeautifulSoup(src, "lxml")
    all_products_hrefs = bs.find_all(class_ = "mzr-tc-group-item-href")
    
    products = {}
    for product in all_products_hrefs:
        products[product.text] = "https://health-diet.ru" + product.get("href")
        print("{0}: {1}".format(product.text, "https://health-diet.ru" + product.get("href")))
    
    with open("products.json", "w") as file:
        json.dump(products, file, indent = 4, ensure_ascii = False)
        
