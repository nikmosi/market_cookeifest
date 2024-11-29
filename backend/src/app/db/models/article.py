from __future__ import annotations

from pydantic import BaseModel


class Option(BaseModel):
    name: str
    value: str
    charc_type: int
    is_variable: bool | None = None


class Composition(BaseModel):
    name: str


class Certificate(BaseModel):
    verified: bool


class FullColor(BaseModel):
    nm_id: int


class Selling(BaseModel):
    no_return_map: int
    brand_name: str
    brand_hash: str
    supplier_id: int


class Media(BaseModel):
    photo_count: int


class Data(BaseModel):
    subject_id: int
    subject_root_id: int
    chrt_ids: list[int]
    tech_size: str


class GroupedOption(BaseModel):
    group_name: str
    options: list[Option]


class Article(BaseModel):
    imt_id: int
    nm_id: int
    imt_name: str
    slug: str
    subj_name: str
    subj_root_name: str
    vendor_code: str
    description: str
    options: list[Option]
    compositions: list[Composition]
    certificate: Certificate
    colors: list[int]
    contents: str
    full_colors: list[FullColor]
    selling: Selling
    media: Media
    data: Data
    grouped_options: list[GroupedOption]
