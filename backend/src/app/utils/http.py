import asyncio

import httpx
from loguru import logger

from app.alib.exceptions import RetryError


async def fetch_url(
    client: httpx.AsyncClient, url: str, retries: int = 3, timeout: float = 10.0
) -> httpx.Response:
    for attempt in range(retries):
        try:
            logger.debug(f"{url}")
            response = await client.get(url, timeout=timeout)
            return response
        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}, attempt {attempt + 1}")
            if attempt == retries - 1:
                logger.error(f"Max retries reached for {url}")
                raise RetryError(url, retries) from None
            await asyncio.sleep(1)
    raise RetryError(url, retries) from None
