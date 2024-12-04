from loguru import logger

from app.data import config

from .connection import client
from .promt import search_query_prompt


async def product_validation(productInfo):
    item = productInfo[0]
    logger.debug(f"{item}")
    result = f"""
Название: {item['name']}
Описание: {item['description']}
Опции: {', '.join([f"{key}: {value}" for key, value in item['options'].items()])}
"""
    logger.debug(f"{result=}")
    response = await client.chat(
        model=config.ollama.model,
        messages=[
            {"role": "system", "content": search_query_prompt},
            {"role": "user", "content": result},
        ],
    )

    logger.debug(response["message"]["content"])
    return response["message"]["content"]
