#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Literal, Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict, RootModel, model_validator

from domain.exceptions import ValidationError


class AttributeSchema(BaseModel):
    id: int = Field(
        ...,
        description="Attribute ID"
    )

    server_id: int = Field(
        ...,
        description="Server ID"
    )

    key: str = Field(
        ...,
        description="Attribute key"
    )

    value: str = Field(
        ...,
        description="Attribute value"
    )

    created_at: datetime = Field(
        ...,
        description="Creation timestamp"
    )

    updated_at: datetime = Field(
        ...,
        description="Last update timestamp"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "id": 1,
                "server_id": 1,
                "key": "motd",
                "value": "Welcome to the server!",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T12:00:00"
            }
        }
    )

class AttributesPageSchema(BaseModel):
    attributes: List[AttributeSchema] = Field(
        ...,
        description="List of attributes"
    )

    total: int = Field(
        ...,
        description="Total number of attributes"
    )

    page: int = Field(
        ...,
        description="Current page"
    )

    pages: int = Field(
        ...,
        description="Total number of pages"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "attributes": [
                    {
                        "id": 1,
                        "server_id": 1,
                        "key": "motd",
                        "value": "Welcome to the server!",
                        "created_at": "2024-01-01T12:00:00",
                        "updated_at": "2024-01-02T12:00:00"
                    }
                ],
                "total": 5,
                "page": 1,
                "pages": 1
            }
        }
    )

class AttributesGetPageSchema(BaseModel):
    page: int = Field(
        1,
        gt=0,
        description="Page number"
    )

    search: Optional[str] = Field(
        None,
        max_length=100,
        description="Search query (by key or value)"
    )

    sort_field: Literal["id", "key", "value", "created_at", "updated_at"] = Field(
        "id",
        description="Field to sort by"
    )

    sort_direction: Literal["asc", "desc"] = Field(
        "desc",
        description="Sort direction"
    )

    limit: int = Field(
        10,
        gt=0,
        le=100,
        description="Number of items per page"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "page": 1,
                "search": "motd",
                "sort_field": "id",
                "sort_direction": "desc",
                "limit": 10
            }
        }
    )

class AttributeCreateSchema(BaseModel):
    key: str = Field(
        ...,
        min_length=1,
        max_length=64,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Attribute key"
    )

    value: str = Field(
        ...,
        description="Attribute value"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "key": "motd",
                "value": "Welcome to the server!"
            }
        }
    )

class AttributeUpdateSchema(BaseModel):
    key: Optional[str] = Field(
        None,
        min_length=1,
        max_length=64,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Attribute key"
    )

    value: Optional[str] = Field(
        None,
        description="New attribute value"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "key": "motd",
                "value": "Updated server message!"
            }
        }
    )

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        if not any([self.key, self.value]):
            raise ValidationError("At least one field (key or value) must be provided")
        return self

class AttributesUpdateSchema(AttributeUpdateSchema):
    id: int = Field(
        ...,
        description="Attribute ID"
    )

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "id": 1,
                "key": "motd",
                "value": "Updated server message!"
            }
        }
    )

class AttributesDeleteSchema(RootModel):
    root: List[Annotated[int, Field(gt=0)]] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of attribute IDs to delete"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": [
                1,
                2
            ]
        }
    )
