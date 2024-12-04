from __future__ import annotations

from pydantic import BaseModel


class Option(BaseModel):
    name: str
    value: str
    charc_type: int
    is_variable: bool | None = None
    variable_values: list[str] | None = None


class Composition(BaseModel):
    name: str


class Value(BaseModel):
    tech_size: str
    chrt_id: int
    details: list[str]


class SizesTable(BaseModel):
    details_props: list[str]
    values: list[Value]


class Certificate(BaseModel):
    verified: bool


class FullColor(BaseModel):
    nm_id: int


class Selling(BaseModel):
    brand_name: str
    brand_hash: str
    supplier_id: int


class Media(BaseModel):
    has_video: bool
    photo_count: int


class Data(BaseModel):
    subject_id: int
    subject_root_id: int
    chrt_ids: list[int]


class GroupedOption(BaseModel):
    group_name: str
    options: list[Option]


class WbArticle(BaseModel):
    imt_id: int
    nm_id: int
    has_rich: bool
    imt_name: str
    slug: str
    subj_name: str
    subj_root_name: str
    vendor_code: str
    description: str
    options: list[Option]
    compositions: list[Composition]
    sizes_table: SizesTable
    certificate: Certificate
    nm_colors_names: str
    colors: list[int]
    contents: str
    full_colors: list[FullColor]
    selling: Selling
    media: Media
    data: Data
    grouped_options: list[GroupedOption]
