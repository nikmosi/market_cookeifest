import os

from loguru import logger

from .connection import client
from .promt import search_query_prompt

model = os.getenv("OLLAMA_MODEL", "llama3.1")


async def product_validation(productInfo):
    item = productInfo[0]
    logger.debug(f"{item}")
    result = f"""
Название: {item['name']}
Описание: {item['description']}
Опции: {', '.join([f"{key}: {value}" for key, value in item['options'].items()])}
"""
    logger.debug(f"{result=}")
    logger.debug(model)
    response = await client.chat(
        model=model,
        messages=[
            {"role": "system", "content": search_query_prompt},
            {"role": "user", "content": result},
        ],
    )

    logger.debug(response["message"]["content"])
    return response["message"]["content"]
