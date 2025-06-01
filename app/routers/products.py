



from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Product, User
from app.schemas.schema import ProductCreate, ProductUpdate, ProductOut
from app.auth.auth import get_db, get_current_user

router = APIRouter()


@router.post(
    "/",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create products",
        )

    new_product = Product(**product.dict())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@router.get(
    "/",
    response_model=List[ProductOut],
    summary="Get all products (with optional search filters)",
)
async def get_products(
    name: Optional[str] = Query(None, description="Search by product name"),
    category: Optional[str] = Query(None, description="Filter by category name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    query = select(Product).options(joinedload(Product.category))

    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))

    if category:
        query = query.join(Product.category).where(Product.category.has(name=category))

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    products = result.scalars().all()
    return products


@router.get(
    "/{product_id}",
    response_model=ProductOut,
    summary="Get product by ID",
)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Product).options(joinedload(Product.category)).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.put(
    "/{product_id}",
    response_model=ProductOut,
    summary="Update a product by ID",
)
async def update_product(
    product_id: int,
    updated_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update products",
        )

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    for field, value in updated_data.dict(exclude_unset=True).items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    # Re-fetch the product with joinedload for category to avoid lazy loading error
    result = await db.execute(
        select(Product).options(joinedload(Product.category)).where(Product.id == product_id)
    )
    updated_product = result.scalar_one()

    return updated_product



@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product by ID",
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete products",
        )

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    await db.delete(product)
    await db.commit()
