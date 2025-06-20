import json, logging
from datetime import datetime
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.routers.mpesa_auth import send_stk_push
from app.models.models import Payment

router = APIRouter(prefix="/payments", tags=["Payments"])
log    = logging.getLogger(__name__)

@router.post("/stk-push")
async def initiate_payment(
    phone: str,
    amount: float,
    order_id: int,
    db: AsyncSession = Depends(get_db),   # ✅ real session now
):
    try:
        resp = await send_stk_push(phone, amount, order_id, db)
        return {
            "message": "STK push sent; await callback",
            "merchant_request_id": resp.get("MerchantRequestID"),
            "checkout_request_id": resp.get("CheckoutRequestID"),
        }
    except Exception as err:
        log.error("STK push initiation error", exc_info=True)
        raise HTTPException(500, f"Failed to initiate STK push: {err}")




@router.post("/callback")
async def mpesa_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        raw = await request.body()
        if not raw:
            raise HTTPException(400, "Empty callback body")

        data = json.loads(raw.decode())
        log.info("🔁 Raw Callback JSON: %s", data)

        cb = data["Body"]["stkCallback"]
        cid = cb["CheckoutRequestID"]

    except json.JSONDecodeError as e:
        log.error("❌ Callback JSON error: %s", e)
        raise HTTPException(400, "Invalid JSON in callback payload")
    except KeyError:
        raise HTTPException(400, "Malformed callback payload")

    # Find payment
    q = await db.execute(select(Payment).filter_by(checkout_request_id=cid))
    pay = q.scalars().first()
    if not pay:
        return {"message": "Payment not found"}

    # Update payment
    if cb["ResultCode"] == 0:
     meta = {i["Name"]: i.get("Value") for i in cb["CallbackMetadata"]["Item"]}
     pay.status = "COMPLETED"
     pay.mpesa_receipt_number = meta.get("MpesaReceiptNumber")
     pay.amount = meta.get("Amount")
     pay.phone_number = str(meta.get("PhoneNumber"))  # 👈 Fix here
     pay.transaction_date = datetime.utcnow()
    else:
     pay.status = "FAILED"


    pay.updated_at = datetime.utcnow()
    await db.commit()

    return {"message": "Callback processed", "status": pay.status}
