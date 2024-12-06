from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    time2: int

    model_config = ConfigDict(extra="allow")


class Data(BaseModel):
    products: list[Product]


class WbDelivery(BaseModel):
    state: int
    payloadVersion: int
    data: Data
