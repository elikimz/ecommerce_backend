from typing import List

def generate_order_email_body(
    customer_name: str,
    email: str,
    phone: str,
    shipping: str,
    total: float,
    items: List[dict],
) -> str:
    item_blocks = ""
    for item in items:
        img_tag = (
            f'<img src="{item["image_url"]}" alt="{item["name"]}" '
            f'style="width:120px;height:auto;border-radius:8px;margin-right:12px;" />'
            if item.get("image_url")
            else ""
        )

        item_blocks += f"""
        <div style="display:flex;align-items:center;padding:12px;background:#fff;border-radius:8px;
                    box-shadow:0 2px 4px rgba(0,0,0,0.05);margin-bottom:12px;">
            {img_tag}
            <div style="flex:1;">
                <div style="font-size:16px;font-weight:600;color:#333;">{item['name']}</div>
                <div style="color:#555;">Qty: {item['quantity']}</div>
                <div style="color:#555;">Price: <strong>KES {item['price']}</strong></div>
            </div>
        </div>
        """

    return f"""
    <div style="max-width:600px;margin:auto;background:#f4f4f4;padding:20px;border-radius:12px;
                font-family:sans-serif;color:#333;">
        <h2 style="color:#f97316;">🛒 New Order Received</h2>

        <p><strong>Name:</strong> {customer_name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Shipping Address:</strong> {shipping}</p>
        <p><strong>Total Amount:</strong> <span style="color:#f97316;font-weight:bold;">KES {total}</span></p>

        <h3 style="margin-top:24px;color:#f97316;">🧾 Order Items</h3>
        {item_blocks}

        <p style="text-align:center;margin-top:24px;font-size:13px;color:#888;">
            Thank you for using TechGiants – your trusted eCommerce platform!
        </p>
    </div>
    """
