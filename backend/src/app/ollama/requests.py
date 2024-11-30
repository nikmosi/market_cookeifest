import json
import os

from .connection import client
from .promt import product_validation_prompt, search_query_prompt

model = os.getenv("OLLAMA_MODEL", "llama3.1")


def product_validation(productInfo):
    return "шорты"
    msg = json.dumps(json.dumps(productInfo))
    print(model)
    response = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": search_query_prompt},
            {"role": "user", "content": msg},
        ],
    )
    return response["message"]["content"]


def search_alternative(productInfo, alternativeProductInfo):
    response = client.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": product_validation_prompt(productInfo),
            },
            {
                "role": "user",
                "content": alternativeProductInfo,
            },
        ],
    )
    return response["message"]["content"]
