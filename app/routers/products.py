




from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Product, ProductImage, ProductVideo, User
from app.schemas.schema import ProductCreate, ProductUpdate, ProductOut
from app.auth.auth import get_db, get_current_user

router = APIRouter()

# ────────────────────────────────────────────────────────────────
# CREATE PRODUCT
# ────────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product (supports multiple images & videos)",
)
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only admins
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can create products")

    # 1) Insert base product (thumbnail remains in image_url if provided)
    new_product = Product(**payload.dict(exclude={"image_urls", "video_urls"}))
    db.add(new_product)
    await db.flush()  # obtain new_product.id

    # 2) Convert HttpUrl → str and insert child rows
    image_urls = [str(url) for url in payload.image_urls or []]
    video_urls = [str(url) for url in payload.video_urls or []]

    db.add_all([ProductImage(url=url, product_id=new_product.id) for url in image_urls])
    db.add_all([ProductVideo(url=url, product_id=new_product.id) for url in video_urls])

    await db.commit()
    await db.refresh(new_product)

    # 3) Return product with eager‑loaded relations
    result = await db.execute(
        select(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.images),
            joinedload(Product.videos),
        )
        .where(Product.id == new_product.id)
    )
    return result.unique().scalar_one()


# ────────────────────────────────────────────────────────────────
# GET ALL PRODUCTS
# ────────────────────────────────────────────────────────────────
@router.get("/", response_model=List[ProductOut], summary="Get all products")
async def get_products(
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.images),
            joinedload(Product.videos),
        )
        .offset(skip)
        .limit(limit)
    )

    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))
    if category:
        query = query.join(Product.category).where(Product.category.has(name=category))

    result = await db.execute(query)
    return result.unique().scalars().all()


# ────────────────────────────────────────────────────────────────
# GET PRODUCT BY ID
# ────────────────────────────────────────────────────────────────
@router.get("/{product_id}", response_model=ProductOut, summary="Get product by ID")
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.images),
            joinedload(Product.videos),
        )
        .where(Product.id == product_id)
    )
    product = result.unique().scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# ────────────────────────────────────────────────────────────────
# UPDATE PRODUCT
# ────────────────────────────────────────────────────────────────
@router.put("/{product_id}", response_model=ProductOut, summary="Update a product")
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can update products")

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 1) Update scalar fields
    for field, value in payload.dict(exclude_unset=True, exclude={"image_urls", "video_urls"}).items():
        setattr(product, field, value)

    # 2) Replace images if provided
    if payload.image_urls is not None:
        await db.execute(delete(ProductImage).where(ProductImage.product_id == product_id))
        db.add_all(
            [ProductImage(url=str(url), product_id=product_id) for url in payload.image_urls]
        )

    # 3) Replace videos if provided
    if payload.video_urls is not None:
        await db.execute(delete(ProductVideo).where(ProductVideo.product_id == product_id))
        db.add_all(
            [ProductVideo(url=str(url), product_id=product_id) for url in payload.video_urls]
        )

    await db.commit()

    # 4) Return updated product with relations
    result = await db.execute(
        select(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.images),
            joinedload(Product.videos),
        )
        .where(Product.id == product_id)
    )
    return result.unique().scalar_one()


# ────────────────────────────────────────────────────────────────
# DELETE PRODUCT
# ────────────────────────────────────────────────────────────────
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a product")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can delete products")

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    

    await db.delete(product)
    await db.commit()
