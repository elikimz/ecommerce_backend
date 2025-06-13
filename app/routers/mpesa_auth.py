import httpx
from base64 import b64encode
from datetime import datetime
from os import getenv
from fastapi import HTTPException

MPESA_BASE_URL = getenv("MPESA_BASE_URL")
CONSUMER_KEY = getenv("MPESA_CONSUMER_KEY")
CONSUMER_SECRET = getenv("MPESA_CONSUMER_SECRET")
SHORTCODE = getenv("MPESA_SHORTCODE")
PASSKEY = getenv("MPESA_PASSKEY")
CALLBACK_URL = getenv("MPESA_CALLBACK_URL")

async def get_mpesa_access_token() -> str:
    url = f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
    auth = b64encode(credentials.encode()).decode()

    headers = {"Authorization": f"Basic {auth}"}

    print(f"Requesting M-Pesa access token from: {url}")

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    print(f"Access token response status: {response.status_code}")
    print(f"Access token response body: {response.text}")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get M-Pesa access token")

    return response.json().get("access_token")


async def send_stk_push(phone_number: str, amount: float, order_id: int):
    print(f"Starting STK Push for phone: {phone_number}, amount: {amount}, order_id: {order_id}")
    
    access_token = await get_mpesa_access_token()
    print("Access token acquired.")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = b64encode(f"{SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()

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
        "TransactionDesc": "Payment for order",
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"
    print(f"Sending STK Push to: {url}")
    print("STK Payload:", payload)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    print(f"STK push response status: {response.status_code}")
    print(f"STK push response body: {response.text}")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="STK Push failed")

    return response.json()
