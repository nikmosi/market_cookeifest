from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    name: str
    catalog_type: str
    catalog_value: str
    rmi: str
    rs: int
    title: str
    search_result: dict[str, Any]


class Color(BaseModel):
    name: str
    id: int


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
    wh: int
    time1: int
    time2: int
    dtype: int
    price: Price
    saleConditions: int
    payload: str


class Product(BaseModel):
    msort: int = Field(alias="__msort")
    mrel: int
    mksort: int
    logs: str
    time1: int
    time2: int
    wh: int
    dtype: int
    dist: int
    id: int
    root: int
    kindId: int
    brand: str
    brandId: int
    siteBrandId: int
    colors: list[Color]
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
    sizes: list[Size]
    totalQuantity: int
    meta: dict[str, Any]


class Data(BaseModel):
    products: list[Product]
    total: int


class WbProduct(BaseModel):
    metadata: Metadata
    state: int
    version: int
    payloadVersion: int
    data: Data
