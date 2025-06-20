from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import os

from app.models.models import Order, OrderItem, User, Product
from app.schemas.schema import OrderCreate, OrderUpdate, OrderOut
from app.auth.auth import get_db, get_current_user
from app.EMail.email_service import send_email
from app.EMail.email_templates import generate_order_email_body

router = APIRouter()

# Eager loading for nested product data
product_loader = (
    selectinload(Order.order_items)
    .selectinload(OrderItem.product)
    .options(
        selectinload(Product.category),
        selectinload(Product.images),
        selectinload(Product.videos),
    )
)

# --------------------------------------------------------------------------- #
#                               CREATE ORDER                                  #
# --------------------------------------------------------------------------- #
# @router.post(
#     "/orders",
#     response_model=OrderOut,
#     status_code=status.HTTP_201_CREATED,
#     summary="Create a new order",
# )
# async def create_order(
#     order: OrderCreate,
#     background_tasks: BackgroundTasks,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     # 1️⃣  Build order + items (in‑memory)
#     new_order = Order(
#         user_id=current_user.id,
#         customer_name=order.customer_name,
#         customer_email=order.customer_email,
#         customer_phone=order.customer_phone,
#         total_amount=order.total_amount,
#         shipping_address=order.shipping_address,
#         status="pending",
#     )

#     order_items_entities = [
#         OrderItem(
#             product_id=i.product_id,
#             quantity=i.quantity,
#             price=i.price,
#         )
#         for i in order.order_items
#     ]
#     new_order.order_items = order_items_entities

#     db.add(new_order)
#     await db.flush()  # Get order ID before commit

#     # 2️⃣  Fetch product info with images and build email details
#     item_details: List[dict] = []
#     for oi in order_items_entities:
#         res = await db.execute(
#             select(Product).options(selectinload(Product.images)).where(Product.id == oi.product_id)
#         )
#         product = res.scalar_one()
#         image_url = product.images[0].url if product.images else ""
#         item_details.append(
#             {
#                 "name": product.name,
#                 "quantity": oi.quantity,
#                 "price": oi.price,
#                 "image_url": image_url,
#             }
#         )

#     # 3️⃣  Commit and refresh the order
#     await db.commit()
#     await db.refresh(new_order)

#     # 4️⃣  Send background email to admin
#     admin_email = os.getenv("ADMIN_EMAIL")
#     if not admin_email:
#         raise HTTPException(status_code=500, detail="ADMIN_EMAIL not configured")

#     email_body = generate_order_email_body(
#         customer_name=new_order.customer_name,
#         email=new_order.customer_email,
#         phone=new_order.customer_phone,
#         shipping=new_order.shipping_address,
#         total=new_order.total_amount,
#         items=item_details,
#     )

#     background_tasks.add_task(
#         send_email,
#         admin_email,
#         f"New Order #{new_order.id} from {new_order.customer_name}",
#         email_body,
#     )

#     # 5️⃣  Return created order
#     res = await db.execute(
#         select(Order).options(product_loader).where(Order.id == new_order.id)
#     )
#     return res.scalar_one()


# app/api/routes/orders.py

@router.post(
    "/orders",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
)
async def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Create order and items
    new_order = Order(
        user_id=current_user.id,
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,
        total_amount=order.total_amount,
        shipping_address=order.shipping_address,
        status="pending",
    )
    order_items_entities = [
        OrderItem(product_id=i.product_id, quantity=i.quantity, price=i.price)
        for i in order.order_items
    ]
    new_order.order_items = order_items_entities

    db.add(new_order)
    await db.flush()

    # 2. Fetch product images and build item details
    item_details: List[dict] = []
    for oi in order_items_entities:
        res = await db.execute(
            select(Product).options(selectinload(Product.images)).where(Product.id == oi.product_id)
        )
        product = res.scalar_one()
        image_url = product.images[0].url if product.images else ""
        item_details.append(
            {
                "name": product.name,
                "quantity": oi.quantity,
                "price": oi.price,
                "image_url": image_url,
            }
        )

    await db.commit()
    await db.refresh(new_order)

    # 3. Send email to both admin and customer
    admin_email = os.getenv("ADMIN_EMAIL")
    if not admin_email:
        raise HTTPException(status_code=500, detail="ADMIN_EMAIL not configured")

    email_body = generate_order_email_body(
        customer_name=new_order.customer_name,
        email=new_order.customer_email,
        phone=new_order.customer_phone,
        shipping=new_order.shipping_address,
        total=new_order.total_amount,
        items=item_details,
    )

    recipients = [admin_email, new_order.customer_email]
    subject = f"Order #{new_order.id} from {new_order.customer_name}"

    background_tasks.add_task(send_email, subject, recipients, email_body)

    # 4. Return created order
    res = await db.execute(
        select(Order).options(product_loader).where(Order.id == new_order.id)
    )
    return res.scalar_one()


# --------------------------------------------------------------------------- #
#                               GET ORDERS                                    #
# --------------------------------------------------------------------------- #
@router.get("/orders", response_model=List[OrderOut], summary="Get all orders")
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Order).options(product_loader)
    if current_user.role.upper() != "ADMIN":
        query = query.where(Order.user_id == current_user.id)
    res = await db.execute(query.offset(skip).limit(limit))
    return res.scalars().all()

# --------------------------------------------------------------------------- #
#                           GET MY ORDERS                                     #
# --------------------------------------------------------------------------- #
@router.get("/orders/me", response_model=List[OrderOut], summary="Get my orders")
async def get_my_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    res = await db.execute(
        select(Order)
        .options(product_loader)
        .where(Order.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    return res.scalars().all()

# --------------------------------------------------------------------------- #
#                        GET ORDER BY ID                                      #
# --------------------------------------------------------------------------- #
@router.get("/orders/{order_id}", response_model=OrderOut, summary="Get order by ID")
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    res = await db.execute(
        select(Order).options(product_loader).where(Order.id == order_id)
    )
    order_obj = res.scalar_one_or_none()
    if not order_obj:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role.upper() != "ADMIN" and order_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return order_obj

# --------------------------------------------------------------------------- #
#                            UPDATE ORDER                                     #
# --------------------------------------------------------------------------- #
@router.put("/orders/{order_id}", response_model=OrderOut, summary="Update order")
async def update_order(
    order_id: int,
    updated: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    res = await db.execute(
        select(Order).options(product_loader).where(Order.id == order_id)
    )
    order_obj = res.scalar_one_or_none()
    if not order_obj:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role.upper() != "ADMIN" and order_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for field, val in updated.dict(exclude_unset=True).items():
        setattr(order_obj, field, val)

    await db.commit()
    await db.refresh(order_obj)

    res = await db.execute(
        select(Order).options(product_loader).where(Order.id == order_id)
    )
    return res.scalar_one()

# --------------------------------------------------------------------------- #
#                            DELETE ORDER                                     #
# --------------------------------------------------------------------------- #
@router.delete("/orders/{order_id}", status_code=204, summary="Delete order")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    res = await db.execute(select(Order).where(Order.id == order_id))
    order_obj = res.scalar_one_or_none()
    if not order_obj:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role.upper() != "ADMIN" and order_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    await db.delete(order_obj)
    await db.commit()
