# from fastapi import APIRouter, Depends, Request, HTTPException
# from sqlalchemy.orm import Session
# from app.database.connection import get_db
# from app.routers.mpesa_auth import send_stk_push
# from app.models.models import Payment, Order  # Adjust if paths are different
# from datetime import datetime
# import logging

# router = APIRouter()

# # Configure basic logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# @router.post("/stk-push")
# async def initiate_payment(phone: str, amount: float, order_id: int, db: Session = Depends(get_db)):
#     try:
#         response = await send_stk_push(phone, amount, order_id)
#         return {"message": "STK Push initiated", "response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/callback")
# async def mpesa_callback(request: Request, db: Session = Depends(get_db)):
#     payload = await request.json()
#     logger.info(f"Received M-PESA callback: {payload}")

#     callback = payload.get("Body", {}).get("stkCallback", {})
#     result_code = callback.get("ResultCode")

#     if result_code == 0:
#         metadata = callback.get("CallbackMetadata", {}).get("Item", [])
#         receipt = next((item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber"), None)
#         amount = next((item["Value"] for item in metadata if item["Name"] == "Amount"), None)
#         phone = next((item["Value"] for item in metadata if item["Name"] == "PhoneNumber"), None)
#         order_id_str = callback.get("AccountReference", "").replace("Order", "")
#         order_id = int(order_id_str) if order_id_str.isdigit() else None

#         if not all([receipt, amount, phone, order_id]):
#             logger.warning("Missing data in callback")
#             return {"message": "Missing payment data in callback"}

#         order = db.query(Order).filter(Order.id == order_id).first()
#         if not order:
#             logger.warning(f"Order not found with ID: {order_id}")
#             return {"message": "Order not found"}

#         # Save payment
#         payment = Payment(
#             order_id=order_id,
#             amount=amount,
#             payment_method="M-PESA",
#             status="COMPLETED",
#             created_at=datetime.utcnow(),
#             updated_at=datetime.utcnow()
#         )
#         db.add(payment)
#         db.commit()

#         logger.info(f"Payment saved: Order ID {order_id}, Receipt {receipt}, Amount {amount}")
#         return {"message": "Payment successful", "receipt": receipt}

#     else:
#         logger.warning(f"STK Push failed with code {result_code}")
#         return {"message": "Payment failed", "details": callback}





import json
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.routers.mpesa_auth import send_stk_push
from app.models.models import Payment, Order

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/stk-push")
async def initiate_payment(phone: str, amount: float, order_id: int, db: AsyncSession = Depends(get_db)):
    try:
        response = await send_stk_push(phone, amount, order_id)
        logger.info(f"STK Push response: {response}")
        return {"message": "STK Push initiated", "response": response}
    except Exception as e:
        logger.error(f"Error during STK Push initiation: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate STK Push")


@router.post("/callback")
async def mpesa_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        raw_body = await request.body()
        logger.info(f"Raw callback body: {raw_body.decode('utf-8')}")
        payload = json.loads(raw_body)
    except Exception as e:
        logger.error(f"Failed to decode M-PESA callback JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    logger.info(f"Received M-PESA callback: {payload}")

    callback = payload.get("Body", {}).get("stkCallback", {})
    result_code = callback.get("ResultCode")

    if result_code == 0:
        metadata = callback.get("CallbackMetadata", {}).get("Item", [])
        receipt = next((item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber"), None)
        amount = next((item["Value"] for item in metadata if item["Name"] == "Amount"), None)
        phone = next((item["Value"] for item in metadata if item["Name"] == "PhoneNumber"), None)
        order_id_str = callback.get("AccountReference", "").replace("Order", "")
        order_id = int(order_id_str) if order_id_str.isdigit() else None

        if not all([receipt, amount, phone, order_id]):
            logger.warning("Missing data in callback")
            return {"message": "Missing payment data in callback"}

        # Async query to get order
        result = await db.execute(select(Order).filter(Order.id == order_id))
        order = result.scalars().first()

        if not order:
            logger.warning(f"Order not found with ID: {order_id}")
            return {"message": "Order not found"}

        # Save payment
        payment = Payment(
            order_id=order_id,
            amount=amount,
            payment_method="M-PESA",
            status="COMPLETED",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(payment)
        await db.commit()

        logger.info(f"Payment saved: Order ID {order_id}, Receipt {receipt}, Amount {amount}")
        return {"message": "Payment successful", "receipt": receipt}

    else:
        logger.warning(f"STK Push failed with code {result_code}")
        return {"message": "Payment failed", "details": callback}
