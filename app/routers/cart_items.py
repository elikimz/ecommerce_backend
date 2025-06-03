from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import Cart, CartItem, Product, User
from app.auth.auth import get_current_user, get_db
from app.schemas.schema import CartItemCreate, CartItemUpdate

router = APIRouter()

# ADD ITEM TO CART
@router.post("/cart/items", status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    item: CartItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = cart_result.scalar_one_or_none()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item_result = await db.execute(
        select(CartItem)
        .where(CartItem.cart_id == cart.id)
        .where(CartItem.product_id == item.product_id)
    )
    cart_item = item_result.scalar_one_or_none()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)

    await db.commit()
    return {"message": "Item added to cart"}


# UPDATE CART ITEM
@router.put("/cart/items", status_code=status.HTTP_200_OK)
async def update_cart_item(
    item: CartItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = cart_result.scalar_one_or_none()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item_result = await db.execute(
        select(CartItem)
        .where(CartItem.cart_id == cart.id)
        .where(CartItem.product_id == item.product_id)
    )
    cart_item = item_result.scalar_one_or_none()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = item.quantity
    await db.commit()
    return {"message": "Cart item updated"}


# DELETE CART ITEM
@router.delete("/cart/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = cart_result.scalar_one_or_none()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item_result = await db.execute(
        select(CartItem)
        .where(CartItem.cart_id == cart.id)
        .where(CartItem.product_id == product_id)
    )
    cart_item = item_result.scalar_one_or_none()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await db.delete(cart_item)
    await db.commit()
