from __future__ import annotations

from pydantic import BaseModel


class WbGeo(BaseModel):
    latitude: float
    longitude: float
    xinfo: str
    userDataSign: str
    destinations: list[int]
    locale: str
    shard: int
    currency: str
    ip: str
    dt: int
