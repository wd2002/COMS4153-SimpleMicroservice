from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        description="Product name.",
        json_schema_extra={"example": "Columbia University Sweater"},
    )
    description: Optional[str] = Field(
        None,
        description="Detailed product description.",
        json_schema_extra={"example": "Comfortable cotton blend sweater with university logo"},
    )
    sku: str = Field(
        ...,
        description="Stock Keeping Unit (SKU) - unique product identifier.",
        json_schema_extra={"example": "CU-SWEATER-001"},
    )
    price: Decimal = Field(
        ...,
        description="Regular price of the product.",
        json_schema_extra={"example": "45.99"},
    )
    sale_price: Optional[Decimal] = Field(
        None,
        description="Sale price if the product is on sale.",
        json_schema_extra={"example": "39.99"},
    )
    cost: Optional[Decimal] = Field(
        None,
        description="Cost price for inventory management.",
        json_schema_extra={"example": "25.00"},
    )
    stock_quantity: int = Field(
        ...,
        description="Current stock quantity available.",
        json_schema_extra={"example": 50},
    )
    reorder_level: int = Field(
        ...,
        description="Minimum stock level before reordering.",
        json_schema_extra={"example": 10},
    )
    category_id: UUID = Field(
        ...,
        description="ID of the category this product belongs to.",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    size: Optional[str] = Field(
        None,
        description="Product size (for apparel, etc.).",
        json_schema_extra={"example": "Large"},
    )
    color: Optional[str] = Field(
        None,
        description="Product color.",
        json_schema_extra={"example": "Navy Blue"},
    )
    material: Optional[str] = Field(
        None,
        description="Product material composition.",
        json_schema_extra={"example": "80% Cotton, 20% Polyester"},
    )
    is_active: bool = Field(
        True,
        description="Whether this product is currently available for sale.",
        json_schema_extra={"example": True},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Columbia University Sweater",
                    "description": "Comfortable cotton blend sweater with university logo",
                    "sku": "CU-SWEATER-001",
                    "price": "45.99",
                    "sale_price": "39.99",
                    "cost": "25.00",
                    "stock_quantity": 50,
                    "reorder_level": 10,
                    "category_id": "550e8400-e29b-41d4-a716-446655440000",
                    "size": "Large",
                    "color": "Navy Blue",
                    "material": "80% Cotton, 20% Polyester",
                    "is_active": True,
                },
                {
                    "name": "University Logo Mug",
                    "description": "Ceramic mug with university logo",
                    "sku": "CU-MUG-001",
                    "price": "12.99",
                    "cost": "6.00",
                    "stock_quantity": 100,
                    "reorder_level": 20,
                    "category_id": "660e8400-e29b-41d4-a716-446655440001",
                    "color": "White",
                    "material": "Ceramic",
                    "is_active": True,
                }
            ]
        }
    }


class ProductCreate(ProductBase):
    """Creation payload for a Product."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Columbia University Hoodie",
                    "description": "Warm fleece hoodie with university logo",
                    "sku": "CU-HOODIE-001",
                    "price": "65.99",
                    "cost": "35.00",
                    "stock_quantity": 30,
                    "reorder_level": 5,
                    "category_id": "550e8400-e29b-41d4-a716-446655440000",
                    "size": "Medium",
                    "color": "Gray",
                    "material": "100% Cotton Fleece",
                    "is_active": True,
                }
            ]
        }
    }


class ProductUpdate(BaseModel):
    """Update payload for a Product; supply only fields to change."""
    name: Optional[str] = Field(
        None, 
        description="Product name.", 
        json_schema_extra={"example": "Columbia University Premium Sweater"}
    )
    description: Optional[str] = Field(
        None, 
        description="Product description.", 
        json_schema_extra={"example": "Premium cotton blend sweater"}
    )
    sku: Optional[str] = Field(
        None, 
        description="Product SKU.", 
        json_schema_extra={"example": "CU-SWEATER-002"}
    )
    price: Optional[Decimal] = Field(
        None, 
        description="Product price.", 
        json_schema_extra={"example": "49.99"}
    )
    sale_price: Optional[Decimal] = Field(
        None, 
        description="Sale price.", 
        json_schema_extra={"example": "44.99"}
    )
    cost: Optional[Decimal] = Field(
        None, 
        description="Cost price.", 
        json_schema_extra={"example": "28.00"}
    )
    stock_quantity: Optional[int] = Field(
        None, 
        description="Stock quantity.", 
        json_schema_extra={"example": 75}
    )
    reorder_level: Optional[int] = Field(
        None, 
        description="Reorder level.", 
        json_schema_extra={"example": 15}
    )
    category_id: Optional[UUID] = Field(
        None, 
        description="Category ID.", 
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"}
    )
    size: Optional[str] = Field(
        None, 
        description="Product size.", 
        json_schema_extra={"example": "Extra Large"}
    )
    color: Optional[str] = Field(
        None, 
        description="Product color.", 
        json_schema_extra={"example": "Black"}
    )
    material: Optional[str] = Field(
        None, 
        description="Product material.", 
        json_schema_extra={"example": "90% Cotton, 10% Spandex"}
    )
    is_active: Optional[bool] = Field(
        None, 
        description="Product active status.", 
        json_schema_extra={"example": False}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"price": "49.99", "sale_price": "44.99"},
                {"stock_quantity": 75, "reorder_level": 15},
                {"is_active": False},
            ]
        }
    }


class ProductRead(ProductBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Product ID.",
        json_schema_extra={"example": "770e8400-e29b-41d4-a716-446655440002"},
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
                    "id": "770e8400-e29b-41d4-a716-446655440002",
                    "name": "Columbia University Sweater",
                    "description": "Comfortable cotton blend sweater with university logo",
                    "sku": "CU-SWEATER-001",
                    "price": "45.99",
                    "sale_price": "39.99",
                    "cost": "25.00",
                    "stock_quantity": 50,
                    "reorder_level": 10,
                    "category_id": "550e8400-e29b-41d4-a716-446655440000",
                    "size": "Large",
                    "color": "Navy Blue",
                    "material": "80% Cotton, 20% Polyester",
                    "is_active": True,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
