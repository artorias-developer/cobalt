#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict, RootModel

from domain.enums import (
    SortDirectionEnum,
    AttributeSortFieldEnum
)


class AttributeSchema(BaseModel):
    id: int = Field(
        ...,
        title="Attribute id",
        description="Attribute ID"
    )

    server_id: int = Field(
        ...,
        title="Server id",
        description="Server ID"
    )

    key: str = Field(
        ...,
        title="Attribute key",
        description="Attribute key"
    )

    value: str = Field(
        ...,
        title="Attribute value",
        description="Attribute value"
    )

    created_at: datetime = Field(
        ...,
        title="Created at",
        description="Creation timestamp"
    )

    updated_at: datetime = Field(
        ...,
        title="Updated at",
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
        title="Attributes",
        description="List of attributes"
    )

    total: int = Field(
        ...,
        title="Total",
        description="Total number of attributes"
    )

    page: int = Field(
        ...,
        title="Page",
        description="Current page"
    )

    pages: int = Field(
        ...,
        title="Pages",
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
        title="Page",
        description="Page number"
    )

    search: Optional[str] = Field(
        None,
        title="Search",
        description="Search query (by key or value)"
    )

    sort_field: AttributeSortFieldEnum = Field(
        AttributeSortFieldEnum.ID,
        title="Sort field",
        description="Field to sort by"
    )

    sort_direction: SortDirectionEnum = Field(
        SortDirectionEnum.DESC,
        title="Sort direction",
        description="Sort direction"
    )

    limit: int = Field(
        10,
        title="Limit",
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
        title="Attribute key",
        description="Attribute key"
    )

    value: str = Field(
        ...,
        title="Attribute value",
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
        title="Attribute key",
        description="Attribute key"
    )

    value: Optional[str] = Field(
        None,
        title="Attribute value",
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

class AttributesUpdateSchema(AttributeUpdateSchema):
    id: int = Field(
        ...,
        title="Attribute id",
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
    root: List[int] = Field(
        ...,
        title="Attribute ids",
        description="List of attribute IDs to delete"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": [1, 2, 3]
        }
    )
