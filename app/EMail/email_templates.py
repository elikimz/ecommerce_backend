from typing import List

def generate_order_email_body(
    customer_name: str,
    email: str,
    phone: str,
    shipping: str,
    total: float,
    items: List[dict],
) -> str:
    """Return a styled HTML order‑notification email."""
    # Build each item block with thumbnail
    item_blocks = ""
    for item in items:
        img_tag = (
            f'<img src="{item["image_url"]}" alt="{item["name"]}" '
            f'style="width:110px;height:auto;border-radius:8px;margin-right:14px;" />'
            if item.get("image_url")
            else ""
        )

        item_blocks += f"""
        <div style="display:flex;align-items:center;padding:12px 14px;background:#fff;border-radius:10px;
                    box-shadow:0 2px 5px rgba(0,0,0,0.06);margin-bottom:14px;">
            {img_tag}
            <div style="flex:1;">
                <div style="font-size:15px;font-weight:600;color:#222;">{item['name']}</div>
                <div style="color:#555;font-size:14px;">Qty: {item['quantity']}</div>
                <div style="color:#555;font-size:14px;">
                    Price: <strong style="color:#f97316;">KES {item['price']}</strong>
                </div>
            </div>
        </div>
        """

    # Main email wrapper
    return f"""
    <div style="max-width:620px;margin:auto;background:#fafafa;padding:28px;border-radius:14px;
                font-family:Arial,Helvetica,sans-serif;color:#333;">
        <!-- Header -->
        <h2 style="color:#f97316;margin-top:0;margin-bottom:10px;">🛒 New Order Received</h2>

        <!-- Customer / shipping details -->
        <p style="margin:4px 0;"><strong>Name:</strong> {customer_name}</p>
        <p style="margin:4px 0;"><strong>Email:</strong> {email}</p>
        <p style="margin:4px 0;"><strong>Phone:</strong> {phone}</p>
        <p style="margin:4px 0;"><strong>Shipping Address:</strong> {shipping}</p>
        <p style="margin:8px 0 20px 0;font-size:16px;">
            <strong>Total Amount:</strong>
            <span style="color:#f97316;font-weight:bold;">KES {total}</span>
        </p>

        <!-- Order items -->
        <h3 style="color:#f97316;margin-bottom:12px;">🧾 Order Items</h3>
        {item_blocks}

        <!-- Thank‑you note -->
        <p style="text-align:center;margin-top:26px;font-size:14px;
                  color:#27ae60;font-weight:600;">
            🎉 Thank you for choosing <span style="color:#f97316;">Smart&nbsp;Indoor&nbsp;Decors</span> –<br/>
            your trusted e‑commerce partner! We hope these items brighten your space. 🌿
        </p>
    </div>
    """
