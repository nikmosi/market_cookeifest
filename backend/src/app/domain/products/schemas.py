from datetime import date

from pydantic import BaseModel, HttpUrl

from app.db.models.article import Article, Option


class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    delivery: date
    rating: float
    reviews_count: int
    options: list[Option]
    images: list[HttpUrl]

    def from_article(self, article: Article) -> "Product":
        return Product(
            id=str(article.nm_id),
            name=article.imt_name,
            description=article.description,
            price=calculate_price(article),
            delivery=calculate_delivery_date(article),
            rating=calculate_rating(article),
            reviews_count=calculate_reviews_count(article),
            options=article.options
            + [
                option
                for grouped in article.grouped_options
                for option in grouped.options
            ],
            images=get_image_urls(article),
        )


class SimilarProducts(BaseModel):
    articles: list[int]
