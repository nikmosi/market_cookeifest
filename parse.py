import requests
import json


#def utf2web(text: str):
    
    

if (__name__ == "__main__"):
    
    
    query = "фен"#input("text: ")
    url = f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-366541&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
    #url = f"https://www.wildberries.ru/catalog/30558977/detail.aspx?targetUrl=EX"
    
    req = requests.get(url)
    src = json.loads(req.text)
    print(src)
    
    
    
    products_list = list(src["data"]["products"])
    for pr in products_list:
        print(pr)
    print(list(src["data"]["products"]))
        
