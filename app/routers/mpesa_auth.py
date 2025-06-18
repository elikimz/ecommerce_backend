import httpx
from base64 import b64encode
from datetime import datetime
from os import getenv
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Payment

MPESA_BASE_URL = getenv("MPESA_BASE_URL")
CONSUMER_KEY   = getenv("MPESA_CONSUMER_KEY")
CONSUMER_SECRET= getenv("MPESA_CONSUMER_SECRET")
SHORTCODE      = getenv("MPESA_SHORTCODE")
PASSKEY        = getenv("MPESA_PASSKEY")
CALLBACK_URL   = getenv("MPESA_CALLBACK_URL")


async def get_mpesa_access_token() -> str:
    url  = f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    auth = b64encode(f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(500, "Failed to get M-Pesa access token")

    return response.json()["access_token"]


async def send_stk_push(phone_number: str, amount: float, order_id: int, db: AsyncSession):
    if db is None:
        raise ValueError("Database session (db) was not provided to send_stk_push")

    access_token = await get_mpesa_access_token()
    timestamp    = datetime.now().strftime("%Y%m%d%H%M%S")
    password     = b64encode(f"{SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": f"Order{order_id}",
        "TransactionDesc": "Order Payment",
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    url = f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(500, "STK Push request failed")

    response_data = response.json()

    # Save payment as PENDING in the database
    payment = Payment(
        order_id=order_id,
        amount=amount,
        payment_method="M-PESA",
        status="PENDING",
        phone_number=phone_number,
        merchant_request_id=response_data.get("MerchantRequestID"),
        checkout_request_id=response_data.get("CheckoutRequestID"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(payment)
    await db.commit()

    return response_data
