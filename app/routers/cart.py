from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.models import Cart, User
from app.auth.auth import get_current_user, get_db
from app.schemas.schema import CartOut

router = APIRouter()

# ========== CREATE CART ==========
@router.post("/", response_model=CartOut, status_code=status.HTTP_201_CREATED)
async def create_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user already has a cart
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    existing_cart = result.scalar_one_or_none()

    if existing_cart:
        raise HTTPException(status_code=400, detail="Cart already exists")

    new_cart = Cart(user_id=current_user.id)
    db.add(new_cart)
    await db.commit()
    await db.refresh(new_cart)
    return new_cart


# ========== GET USER'S CART ==========
@router.get("/", response_model=CartOut)
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Cart)
        .options(selectinload(Cart.cart_items))  # preload items if needed
        .where(Cart.user_id == current_user.id)
    )
    cart = result.scalar_one_or_none()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart


# ========== DELETE USER'S CART ==========
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = result.scalar_one_or_none()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    await db.delete(cart)
    await db.commit()
