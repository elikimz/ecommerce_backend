


from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.schema import UserCreate, UserResponse, Token
from app.database.connection import AsyncSessionLocal
from app.models.models import User
from app.utils.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, generate_otp, 
    get_password_hash, send_otp_email, verify_password,
    SECRET_KEY, ALGORITHM  # Make sure you have these defined in utils.py
)
from jose import JWTError, jwt  # pip install python-jose


# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_db():
    async_db = AsyncSessionLocal()
    try:
        yield async_db
    finally:
        await async_db.close()

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("id")
    if user_id is None:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

# Your existing functions below (register_user, login_for_access_token, etc.) remain unchanged
async def register_user(user: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    result = await db.execute(select(User))
    total_users = result.scalars().all()
    is_first_user = len(total_users) == 0

    hashed_password = get_password_hash(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        address=user.address,
        phone=user.phone,
        role="Admin" if is_first_user else "Customer"
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
    user.otp = None
    user.otp_expires_at = None
    await db.commit()
