from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.database.connection import get_db
from app.models.models import Product

router = APIRouter()

@router.get("/sitemap.xml", response_class=Response, include_in_schema=False)
async def sitemap_xml(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.stock > 0))
    products = result.scalars().all()

    urls = "\n".join([
        f"""<url>
            <loc>https://www.smartindoordecors.com/product/{product.id}</loc>
            <lastmod>{datetime.utcnow().date()}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>""" for product in products
    ])

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://www.smartindoordecors.com/</loc><lastmod>2025-06-28</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>
<url><loc>https://www.smartindoordecors.com/shop</loc><lastmod>2025-06-28</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>
{urls}
</urlset>
"""
    return Response(content=content, media_type="application/xml")
