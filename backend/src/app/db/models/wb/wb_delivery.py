from __future__ import annotations

from pydantic import BaseModel, Field


class Stock(BaseModel):
    wh: int
    dtype: int
    qty: int
    priority: int
    time1: int
    time2: int


class Price(BaseModel):
    basic: int
    product: int
    total: int
    logistics: int
    return_: int = Field(..., alias="return")


class Size(BaseModel):
    name: str
    origName: str
    rank: int
    optionId: int
    stocks: list[Stock]
    time1: int
    time2: int
    wh: int
    dtype: int
    price: Price
    saleConditions: int
    payload: str


class Product(BaseModel):
    id: int
    root: int
    kindId: int
    brand: str
    brandId: int
    siteBrandId: int
    colors: list
    subjectId: int
    subjectParentId: int
    name: str
    entity: str
    supplier: str
    supplierId: int
    supplierRating: float
    supplierFlags: int
    pics: int
    rating: int
    reviewRating: float
    nmReviewRating: float
    feedbacks: int
    nmFeedbacks: int
    volume: int
    viewFlags: int
    promotions: list[int]
    sizes: list[Size]
    totalQuantity: int
    time1: int
    time2: int
    wh: int
    dtype: int


class Data(BaseModel):
    products: list[Product]


class WbDelivery(BaseModel):
    state: int
    payloadVersion: int
    data: Data
