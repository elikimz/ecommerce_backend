from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.database.connection import get_db
from app.models.models import Product

router = APIRouter()

@router.get("/sitemap.xml", response_class=Response)
async def sitemap_xml(db: AsyncSession = Depends(get_db)):
    # Fetch products
    result = await db.execute(select(Product).where(Product.stock > 0))
    products = result.scalars().all()

    # Static routes
    static_routes = [
        {"loc": "https://www.smartindoordecors.com/", "priority": "1.0", "changefreq": "daily"},
        {"loc": "https://www.smartindoordecors.com/shop", "priority": "0.8", "changefreq": "daily"},
        {"loc": "https://www.smartindoordecors.com/about", "priority": "0.5", "changefreq": "monthly"},
        {"loc": "https://www.smartindoordecors.com/blog", "priority": "0.6", "changefreq": "weekly"},
        {"loc": "https://www.smartindoordecors.com/faq", "priority": "0.6", "changefreq": "monthly"},
        {"loc": "https://www.smartindoordecors.com/terms", "priority": "0.4", "changefreq": "yearly"},
        {"loc": "https://www.smartindoordecors.com/privacy", "priority": "0.4", "changefreq": "yearly"},
        {"loc": "https://www.smartindoordecors.com/services", "priority": "0.5", "changefreq": "monthly"},
        {"loc": "https://www.smartindoordecors.com/contact", "priority": "0.5", "changefreq": "monthly"},
        {"loc": "https://www.smartindoordecors.com/testimonials", "priority": "0.5", "changefreq": "monthly"},
    ]

    static_urls = [
        f"""
        <url>
            <loc>{route['loc']}</loc>
            <lastmod>{datetime.utcnow().date()}</lastmod>
            <changefreq>{route['changefreq']}</changefreq>
            <priority>{route['priority']}</priority>
        </url>
        """
        for route in static_routes
    ]

    product_urls = [
        f"""
        <url>
            <loc>https://www.smartindoordecors.com/product/{product.id}</loc>
            <lastmod>{datetime.utcnow().date()}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        """
        for product in products
    ]

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(static_urls)}
{''.join(product_urls)}
</urlset>
"""

    return Response(content=content, media_type="application/xml")
