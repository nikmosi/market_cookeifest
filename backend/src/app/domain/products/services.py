from typing import Any

from loguru import logger

from app.ollama.requests import product_validation


async def generate_optimal_query(article: Any) -> str:
    logger.debug(article)
    return article["name"]
    return await product_validation(article)
