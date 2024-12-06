from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Option(BaseModel):
    name: str
    value: str

    model_config = ConfigDict(extra="allow")


class GroupedOption(BaseModel):
    group_name: str
    options: list[Option]


class WbArticle(BaseModel):
    imt_name: str
    description: str
    options: list[Option]
    grouped_options: list[GroupedOption]

    model_config = ConfigDict(extra="allow")
