from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Option(BaseModel):
    name: str
    value: str
    charc_type: int
    is_variable: Optional[bool] = None


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
    chrt_ids: List[int]
    tech_size: str


class Option1(BaseModel):
    name: str
    value: str
    charc_type: int
    is_variable: Optional[bool] = None


class GroupedOption(BaseModel):
    group_name: str
    options: List[Option1]


class Article(BaseModel):
    imt_id: int
    nm_id: int
    imt_name: str
    slug: str
    subj_name: str
    subj_root_name: str
    vendor_code: str
    description: str
    options: List[Option]
    compositions: List[Composition]
    certificate: Certificate
    colors: List[int]
    contents: str
    full_colors: List[FullColor]
    selling: Selling
    media: Media
    data: Data
    grouped_options: List[GroupedOption]
