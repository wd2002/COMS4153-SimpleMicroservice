from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        description="Category name (e.g., Apparel, Drinkware, Accessories).",
        json_schema_extra={"example": "Apparel"},
    )
    description: Optional[str] = Field(
        None,
        description="Detailed description of the category.",
        json_schema_extra={"example": "University-branded clothing and apparel"},
    )
    is_active: bool = Field(
        True,
        description="Whether this category is currently active for new products.",
        json_schema_extra={"example": True},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Apparel",
                    "description": "University-branded clothing and apparel",
                    "is_active": True,
                },
                {
                    "name": "Drinkware",
                    "description": "Mugs, water bottles, and drink containers",
                    "is_active": True,
                },
                {
                    "name": "Accessories",
                    "description": "Bags, keychains, stickers, and other accessories",
                    "is_active": True,
                }
            ]
        }
    }


class CategoryCreate(CategoryBase):
    """Creation payload for a Category."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Apparel",
                    "description": "University-branded clothing and apparel",
                    "is_active": True,
                }
            ]
        }
    }


class CategoryUpdate(BaseModel):
    """Update payload for a Category; supply only fields to change."""
    name: Optional[str] = Field(
        None, 
        description="Category name.", 
        json_schema_extra={"example": "Clothing & Apparel"}
    )
    description: Optional[str] = Field(
        None, 
        description="Category description.", 
        json_schema_extra={"example": "All university-branded clothing items"}
    )
    is_active: Optional[bool] = Field(
        None, 
        description="Category active status.", 
        json_schema_extra={"example": False}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Clothing & Apparel"},
                {"description": "All university-branded clothing items"},
                {"is_active": False},
            ]
        }
    }


class CategoryRead(CategoryBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Category ID.",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Apparel",
                    "description": "University-branded clothing and apparel",
                    "is_active": True,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
