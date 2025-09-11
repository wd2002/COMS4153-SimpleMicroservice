from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.category import CategoryCreate, CategoryRead, CategoryUpdate
from models.product import ProductCreate, ProductRead, ProductUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
categories: Dict[UUID, CategoryRead] = {}
products: Dict[UUID, ProductRead] = {}

app = FastAPI(
    title="University Bookstore API",
    description="FastAPI microservice for managing bookstore products and categories",
    version="0.0.1",
)

# -----------------------------------------------------------------------------
# Health endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

# -----------------------------------------------------------------------------
# Category endpoints
# -----------------------------------------------------------------------------

@app.post("/categories", response_model=CategoryRead, status_code=201)
def create_category(category: CategoryCreate):
    """Create a new category."""
    category_read = CategoryRead(**category.model_dump())
    categories[category_read.id] = category_read
    return category_read

@app.get("/categories", response_model=List[CategoryRead])
def list_categories(
    name: Optional[str] = Query(None, description="Filter by category name"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
):
    """List all categories with optional filtering."""
    results = list(categories.values())
    
    if name is not None:
        results = [c for c in results if name.lower() in c.name.lower()]
    if is_active is not None:
        results = [c for c in results if c.is_active == is_active]
    
    return results

@app.get("/categories/{category_id}", response_model=CategoryRead)
def get_category(category_id: UUID):
    """Get a specific category by ID."""
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories[category_id]

@app.put("/categories/{category_id}", response_model=CategoryRead)
def update_category(category_id: UUID, update: CategoryUpdate):
    """Update an entire category."""
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Get current category data
    current = categories[category_id].model_dump()
    
    # Update with new data (only provided fields)
    update_data = update.model_dump(exclude_unset=True)
    current.update(update_data)
    
    # Update timestamp
    current["updated_at"] = datetime.utcnow()
    
    # Create new CategoryRead object
    updated_category = CategoryRead(**current)
    categories[category_id] = updated_category
    
    return updated_category

@app.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: UUID):
    """Delete a category."""
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if any products are using this category
    products_using_category = [p for p in products.values() if p.category_id == category_id]
    if products_using_category:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete category. {len(products_using_category)} products are using this category."
        )
    
    del categories[category_id]
    return None

# -----------------------------------------------------------------------------
# Product endpoints
# -----------------------------------------------------------------------------

@app.post("/products", response_model=ProductRead, status_code=201)
def create_product(product: ProductCreate):
    """Create a new product."""
    # Validate that the category exists
    if product.category_id not in categories:
        raise HTTPException(status_code=400, detail="Category not found")
    
    product_read = ProductRead(**product.model_dump())
    products[product_read.id] = product_read
    return product_read

@app.get("/products", response_model=List[ProductRead])
def list_products(
    name: Optional[str] = Query(None, description="Filter by product name"),
    sku: Optional[str] = Query(None, description="Filter by SKU"),
    category_id: Optional[UUID] = Query(None, description="Filter by category ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    low_stock: Optional[bool] = Query(None, description="Filter products with stock below reorder level"),
):
    """List all products with optional filtering."""
    results = list(products.values())
    
    if name is not None:
        results = [p for p in results if name.lower() in p.name.lower()]
    if sku is not None:
        results = [p for p in results if sku.upper() in p.sku.upper()]
    if category_id is not None:
        results = [p for p in results if p.category_id == category_id]
    if is_active is not None:
        results = [p for p in results if p.is_active == is_active]
    if min_price is not None:
        results = [p for p in results if float(p.price) >= min_price]
    if max_price is not None:
        results = [p for p in results if float(p.price) <= max_price]
    if low_stock is not None and low_stock:
        results = [p for p in results if p.stock_quantity <= p.reorder_level]
    
    return results

@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: UUID):
    """Get a specific product by ID."""
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]

@app.put("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: UUID, update: ProductUpdate):
    """Update an entire product."""
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Validate category if being updated
    if update.category_id is not None and update.category_id not in categories:
        raise HTTPException(status_code=400, detail="Category not found")
    
    # Get current product data
    current = products[product_id].model_dump()
    
    # Update with new data (only provided fields)
    update_data = update.model_dump(exclude_unset=True)
    current.update(update_data)
    
    # Update timestamp
    current["updated_at"] = datetime.utcnow()
    
    # Create new ProductRead object
    updated_product = ProductRead(**current)
    products[product_id] = updated_product
    
    return updated_product

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: UUID):
    """Delete a product."""
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    del products[product_id]
    return None

# -----------------------------------------------------------------------------
# Root endpoint
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Welcome to the University Bookstore API. See /docs for OpenAPI UI.",
        "version": "0.0.1"
    }

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
