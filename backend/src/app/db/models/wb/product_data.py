from pydantic import BaseModel, Field


class ProductData(BaseModel):
    id: str = Field(..., description="Unique identifier for the article")
    name: str = Field(..., description="Name of the product")
    description: str = Field(..., description="Description of the product")
    price: float = Field(..., description="Price of the product")
    delivery: str = Field(..., description="Delivery date in DD.MM.YYYY format")
    rating: float = Field(..., description="Review rating of the product")
    reviews_count: int = Field(..., description="Number of reviews")
    options: dict[str, str] = Field(
        ..., description="Dictionary of options for the product"
    )
    images: list[str] = Field(..., description="List of image URLs")
