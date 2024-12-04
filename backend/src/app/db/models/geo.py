from __future__ import annotations

from pydantic import BaseModel


class Geo(BaseModel):
    country_code: str
    country_name: str
    city: str
    postal: str
    latitude: float
    longitude: float
    IPv4: str
    state: str
