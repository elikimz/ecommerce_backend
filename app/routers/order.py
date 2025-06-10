# from typing import List
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload

# from app.models.models import Order, OrderItem, User
# from app.schemas.schema import OrderCreate, OrderUpdate, OrderOut
# from app.auth.auth import get_db, get_current_user

# router = APIRouter()

# @router.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED, summary="Create a new order")
# async def create_order(
#     order: OrderCreate,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     new_order = Order(
#         user_id=current_user.id,
#         total_amount=order.total_amount,
#         shipping_address=order.shipping_address,
#         status=order.status or "pending"
#     )

#     order_items = [
#         OrderItem(product_id=item.product_id, quantity=item.quantity, price=item.price)
#         for item in order.order_items
#     ]
#     new_order.order_items = order_items

#     db.add(new_order)
#     await db.commit()
#     await db.refresh(new_order)

#     # Eagerly load order_items to avoid greenlet issue
#     result = await db.execute(
#         select(Order)
#         .options(selectinload(Order.order_items))
#         .where(Order.id == new_order.id)
#     )
#     order_with_items = result.scalar_one()
#     return order_with_items


# @router.get("/orders", response_model=List[OrderOut], summary="Get all orders")
# async def get_orders(
#     skip: int = 0,
#     limit: int = 100,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     query = select(Order).options(selectinload(Order.order_items))
#     if current_user.role.upper() != "ADMIN":
#         query = query.where(Order.user_id == current_user.id)
#     result = await db.execute(query.offset(skip).limit(limit))
#     return result.scalars().all()


# @router.get("/orders/{order_id}", response_model=OrderOut, summary="Get order by ID")
# async def get_order_by_id(
#     order_id: int,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     result = await db.execute(
#         select(Order)
#         .options(selectinload(Order.order_items))
#         .where(Order.id == order_id)
#     )
#     order = result.scalar_one_or_none()
#     if not order:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
#     if current_user.role.upper() != "ADMIN" and order.user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this order")
#     return order


# @router.put("/orders/{order_id}", response_model=OrderOut, summary="Update an order by ID")
# async def update_order(
#     order_id: int,
#     updated_data: OrderUpdate,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     result = await db.execute(
#         select(Order)
#         .options(selectinload(Order.order_items))
#         .where(Order.id == order_id)
#     )
#     order = result.scalar_one_or_none()
#     if not order:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
#     if current_user.role.upper() != "ADMIN" and order.user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this order")

#     for field, value in updated_data.dict(exclude_unset=True).items():
#         setattr(order, field, value)

#     await db.commit()
#     await db.refresh(order)

#     # Reload with relationships
#     result = await db.execute(
#         select(Order)
#         .options(selectinload(Order.order_items))
#         .where(Order.id == order_id)
#     )
#     return result.scalar_one()


# @router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an order by ID")
# async def delete_order(
#     order_id: int,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     result = await db.execute(select(Order).where(Order.id == order_id))
#     order = result.scalar_one_or_none()
#     if not order:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
#     if current_user.role.upper() != "ADMIN" and order.user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this order")

#     await db.delete(order)
#     await db.commit()










from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import Order, OrderItem, User
from app.schemas.schema import OrderCreate, OrderUpdate, OrderOut
from app.auth.auth import get_db, get_current_user

router = APIRouter()

@router.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED, summary="Create a new order")
async def create_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_order = Order(
        user_id=current_user.id,
        total_amount=order.total_amount,
        shipping_address=order.shipping_address,
        status=order.status or "pending"
    )

    order_items = [
        OrderItem(product_id=item.product_id, quantity=item.quantity, price=item.price)
        for item in order.order_items
    ]
    new_order.order_items = order_items

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    # Eagerly load order_items to avoid greenlet issue
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.order_items))
        .where(Order.id == new_order.id)
    )
    order_with_items = result.scalar_one()
    return order_with_items

@router.get("/orders", response_model=List[OrderOut], summary="Get all orders")
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Order).options(selectinload(Order.order_items))
    if current_user.role.upper() != "ADMIN":
        query = query.where(Order.user_id == current_user.id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/orders/me", response_model=List[OrderOut], summary="Get orders for the current user")
async def get_my_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # This endpoint will always return orders for the current user, regardless of their role
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.order_items))
        .where(Order.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.get("/orders/{order_id}", response_model=OrderOut, summary="Get order by ID")
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.order_items))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if current_user.role.upper() != "ADMIN" and order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this order")
    return order

@router.put("/orders/{order_id}", response_model=OrderOut, summary="Update an order by ID")
async def update_order(
    order_id: int,
    updated_data: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.order_items))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if current_user.role.upper() != "ADMIN" and order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this order")

    for field, value in updated_data.dict(exclude_unset=True).items():
        setattr(order, field, value)

    await db.commit()
    await db.refresh(order)

    # Reload with relationships
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.order_items))
        .where(Order.id == order_id)
    )
    return result.scalar_one()

@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an order by ID")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if current_user.role.upper() != "ADMIN" and order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this order")

    await db.delete(order)
    await db.commit()
