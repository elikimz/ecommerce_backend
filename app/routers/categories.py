from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Category, User  # your models
from app.schemas.schema import CategoryCreate, CategoryUpdate, CategoryOut  # your schemas
from app.auth.auth import get_db, get_current_user  # your dependencies

router = APIRouter()


@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED, summary="Create a new category")
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # if you want auth
):
    # Example: only admin can create categories
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create categories")

    new_category = Category(**category.dict())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


@router.get("/categories", response_model=List[CategoryOut], summary="Get all categories")
async def get_categories(
    skip: int = 0,
    limit: int = 2,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Category).offset(skip).limit(limit))
    categories = result.scalars().all()
    return categories


@router.get("/{category_id}", response_model=CategoryOut, summary="Get category by ID")
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.put("/categories/{category_id}", response_model=CategoryOut, summary="Update a category by ID")
async def update_category(
    category_id: int,
    updated_data: CategoryUpdate,  # Accept request body here
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Optional: Restrict to admins
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can update categories")

    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    # Update fields
    category.name = updated_data.name
    category.description = updated_data.description

    await db.commit()
    await db.refresh(category)

    return category


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a category by ID")
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete categories")

    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    await db.delete(category)
    await db.commit()
    return  # 204 No Content