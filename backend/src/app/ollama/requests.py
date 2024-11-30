import os

import json
from .connection import client
from .promt import search_query_prompt, product_validation_prompt


model = os.getenv("OLLAMA_MODEL", "llama3.1")


def product_validation(productInfo):
    msg = json.dumps(json.dumps(productInfo))
    print(model)
    response = client.chat(
        model=model,
        messages=[
            {"role": "user", "content": "hi water?"},
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
