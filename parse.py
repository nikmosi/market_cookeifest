import requests
import json


def getProductDataByArticle(article: str):
    length = len(article)
    return json.loads(requests.get(f"https://basket-{('0' + article[ : 1]) if (length == 8) else article[ : 2]}.wbbasket.ru/vol{article[ : 3] if (length == 8) else article[ : 5]}/part{article[ : 5] if (length == 8) else article[ : 6]}/{article}/info/ru/card.json").text)

def getProductsByQuery(query: str):
    return json.loads(requests.get(f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false").text)
    

if (__name__ == "__main__"):
    query = "фен"#input("text: ")
    art = "48334378"
    print(getProductDataByArticle("48334378"))
    print(getProductsByQuery(query))
        
