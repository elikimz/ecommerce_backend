
# from datetime import datetime, timedelta
# from fastapi import Depends, HTTPException, status, Request
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from app.schema import UserCreate, UserResponse, Token
# from app.database import AsyncSessionLocal
# from app.models import User
# from app.utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, generate_otp, get_password_hash, send_otp_email, verify_password
# from authlib.integrations.starlette_client import OAuth
# from dotenv import load_dotenv
# import os

# # ✅ Load environment variables from .env
# load_dotenv()

# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# # ✅ Debug prints
# print("GOOGLE_CLIENT_ID:",GOOGLE_CLIENT_ID)
# print("GOOGLE_CLIENT_SECRET:",GOOGLE_CLIENT_SECRET)

# # ✅ OAuth setup using values from .env
# oauth = OAuth()
# oauth.register(
#     name='google',
#     client_id=GOOGLE_CLIENT_ID,
#     client_secret=GOOGLE_CLIENT_SECRET,
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={'scope': 'openid email profile'},
# )

# async def get_db():
#     async_db = AsyncSessionLocal()
#     try:
#         yield async_db
#     finally:
#         await async_db.close()

# async def register_user(user: UserCreate, db: AsyncSession):
#     result = await db.execute(select(User).filter(User.email == user.email))
#     db_user = result.scalars().first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = get_password_hash(user.password)
#     db_user = User(
#         name=user.name,
#         email=user.email,
#         password_hash=hashed_password,
#         address=user.address,
#         phone=user.phone
#     )
#     db.add(db_user)
#     await db.commit()
#     await db.refresh(db_user)
#     return db_user

# async def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
#     result = await db.execute(select(User).filter(User.email == form_data.username))
#     user = result.scalars().first()
#     if not user or not verify_password(form_data.password, user.password_hash):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email,
#               "id": user.id,
#               "fullname": user.name,
#               "role": user.role
#               }, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# async def login_google(request: Request):
#     redirect_uri = request.url_for('auth_google')
#     return await oauth.google.authorize_redirect(request, str(redirect_uri))

# async def auth_google(request: Request, db: AsyncSession):
#     token = await oauth.google.authorize_access_token(request)
#     user_info = await oauth.google.parse_id_token(request, token)

#     email = user_info['email']
#     name = user_info.get('name', '')
#     google_id = user_info.get('sub', '')

#     result = await db.execute(select(User).filter(User.google_id == google_id))
#     user = result.scalars().first()

#     if not user:
#         user = User(
#             name=name,
#             email=email,
#             google_id=google_id,
#             is_google_auth=True
#         )
#         db.add(user)
#         await db.commit()
#         await db.refresh(user)

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email,
#               "id": user.id,
#               "fullname": user.name,
#               "role": user.role
#               }, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# async def request_password_reset(email: str, db: AsyncSession):
#     result = await db.execute(select(User).where(User.email == email))
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     otp = generate_otp()
#     user.otp = otp
#     user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
#     await db.commit()

#     send_otp_email(email, otp)

# async def reset_password(email: str, otp: str, new_password: str, db: AsyncSession):
#     result = await db.execute(select(User).where(User.email == email))
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if user.otp != otp or user.otp_expires_at < datetime.utcnow():
#         raise HTTPException(status_code=400, detail="Invalid or expired OTP")

#     user.password_hash = get_password_hash(new_password)
#     user.otp= None
#     user.otp_expires_at = None
#     await db.commit()



from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.schema import UserCreate, UserResponse, Token
from app.database import AsyncSessionLocal
from app.models import User
from app.utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, generate_otp, get_password_hash, send_otp_email, verify_password

async def get_db():
    async_db = AsyncSessionLocal()
    try:
        yield async_db
    finally:
        await async_db.close()

async def register_user(user: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalars().first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        address=user.address,
        phone=user.phone
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email,
              "id": user.id,
              "fullname": user.name,
              "role": user.role
              }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def request_password_reset(email: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    user.otp = otp
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
    await db.commit()

    send_otp_email(email, otp)

async def reset_password(email: str, otp: str, new_password: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.otp != otp or user.otp_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user.password_hash = get_password_hash(new_password)
    user.otp= None
    user.otp_expires_at = None
    await db.commit()
