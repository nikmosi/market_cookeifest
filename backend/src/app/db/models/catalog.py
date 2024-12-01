from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, root_validator


class Log(BaseModel):
    cpm: int
    promotion: int
    promoPosition: int
    position: int
    advertId: int
    tp: str


class Metadata(BaseModel):
    name: str
    catalog_type: str
    catalog_value: str
    normquery: str
    rmi: str
    rs: int
    title: str
    search_result: dict[str, Any]


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


class Meta(BaseModel):
    presetId: int


class Product(BaseModel):
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
    panelPromoId: int | None = None
    promoTextCard: str | None = None
    promoTextCat: str | None = None
    volume: int
    viewFlags: int
    sizes: list[Size]
    totalQuantity: int
    log: Log | None = None
    logs: list[Log] | None = None
    meta: Meta
    isNew: bool | None = None
    feedbackPoints: int | None = None

    @root_validator(pre=True)
    def ensure_logs_is_list(cls, values):
        logs = values.get("logs")
        if logs and isinstance(logs, str):
            # Assuming 'log_data' needs to be split or parsed
            # Let's say it's base64-encoded JSON or comma-separated data
            logs_data = logs.split(",")  # Or base64 decoding if needed
            # Transform this into individual log fields
            logs = []
            for log_data in logs_data:
                decoded_data = log_data  # You can decode it here if needed
                log = {
                    "cpm": 123,  # Dummy data, replace with actual parsing logic
                    "promotion": 1,  # Dummy
                    "promoPosition": 2,  # Dummy
                    "position": 3,  # Dummy
                    "advertId": 4,  # Dummy
                    "tp": "c",  # Dummy
                }
                logs.append(log)
            values["logs"] = [Log(**log) for log in logs]
        elif logs and not isinstance(logs, list):
            # If logs is not a list, make sure it's converted to a list (you could add additional logic here)
            values["logs"] = [logs]
        return values


class ProductData(BaseModel):
    products: list[Product]
    total: int


class Catalog(BaseModel):
    metadata: Metadata
    state: int
    version: int
    payloadVersion: int
    data: ProductData
