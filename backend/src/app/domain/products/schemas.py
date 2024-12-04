from pydantic import BaseModel


class SimilarProducts(BaseModel):
    articles: list[int]
