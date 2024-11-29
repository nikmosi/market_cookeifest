import requests
import json


#def utf2web(text: str):
    
    

if (__name__ == "__main__"):
    
    
    query = "фен"#input("text: ")
    art = "48334378"
    #url = f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
    url = f"https://basket-{('0' + art[ : 1]) if (len(art) == 8) else art[ : 2]}.wbbasket.ru/vol{art[ : 3] if (len(art) == 8) else art[ : 5]}/part{art[ : 5] if (len(art) == 8) else art[ : 6]}/{art}/info/ru/card.json"
    print(url)
    req = requests.get(url)
    print(req.text)
    src = json.loads(req.text)
    print(src)
    
    
    
    products_list = list(src["data"]["products"])
    for pr in products_list:
        print(pr)
    print(list(src["data"]["products"]))

        
