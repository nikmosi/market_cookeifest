from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class Metadata(BaseModel):
    name: str
    catalog_type: str
    catalog_value: str
    rmi: str
    rs: int
    title: str
    search_result: dict[str, Any]


class Price(BaseModel):
    total: int

    model_config = ConfigDict(extra="allow")


class Size(BaseModel):
    price: Price

    model_config = ConfigDict(extra="allow")


class Product(BaseModel):
    time2: int
    id: int
    name: str
    reviewRating: float
    feedbacks: int
    sizes: list[Size]

    model_config = ConfigDict(extra="allow")


class Data(BaseModel):
    products: list[Product]
    total: int


class WbProduct(BaseModel):
    metadata: Metadata
    state: int
    version: int
    payloadVersion: int
    data: Data
