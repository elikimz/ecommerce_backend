
# import ssl
# import os
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# assert DATABASE_URL is not None, "❌ DATABASE_URL not loaded from .env"

# # Create SSL context
# ssl_context = ssl.create_default_context()
# ssl_context.check_hostname = False
# ssl_context.verify_mode = ssl.CERT_NONE

# # Create engine with SSL context
# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True,
#     connect_args={"ssl": ssl_context}
# )

# AsyncSessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
#     class_=AsyncSession
# )

# Base = declarative_base()

# async def get_db():
#     async with AsyncSessionLocal() as session:

#         yield 
        




import ssl
import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables
load_dotenv()

# Get DB URL
DATABASE_URL = os.getenv("DATABASE_URL")
assert DATABASE_URL is not None, "❌ DATABASE_URL not loaded from .env"

# --- SSL Context (optional for cloud DBs like Supabase or PlanetScale) ---
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# --- Async Engine ---
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    connect_args={"ssl": ssl_context}
)

# --- SessionMaker ---
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

# --- Declarative Base ---
Base = declarative_base()

# --- Dependency for FastAPI routes ---
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# from app.models.models import User,Category,Product,Order,OrderItem,Cart,ProductImage,ProductVideo