




# from typing import List
# from datetime import datetime
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.models.models import User
# from app.schemas.schema import (
#     ForgotPasswordRequest, ResetPasswordRequest,
#     UserCreate, UserResponse, Token, UserUpdate
# )
# from app.auth.auth import (
#     get_db, register_user, login_for_access_token,
#     request_password_reset, reset_password, get_current_user
# )

# router = APIRouter()

# # ✅ Register new user
# @router.post("/register", response_model=UserResponse, summary="Register a new user")
# async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     return await register_user(user, db)

# # ✅ Login to get access token
# @router.post("/login", response_model=Token, summary="Login for access token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
#     return await login_for_access_token(form_data, db)

# # ✅ Request OTP for password reset
# @router.post("/forgot-password", summary="Request OTP for password reset")
# async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
#     await request_password_reset(data.email, db)
#     return {"message": "OTP sent to your email"}

# # ✅ Reset password with OTP
# @router.post("/reset-password", summary="Reset password using OTP")
# async def reset_password_route(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
#     await reset_password(data.email, data.otp, data.new_password, db)
#     return {"message": "Password reset successful"}

# # ✅ Get own profile
# @router.get("/me", response_model=UserResponse, summary="Get current user profile")
# async def get_me(current_user: User = Depends(get_current_user)):
#     return current_user

# # ✅ Update own profile
# @router.put("/update-profile", response_model=UserResponse, summary="Update your own profile")
# async def update_profile(
#     user_update: UserUpdate,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     for field, value in user_update.dict(exclude_unset=True).items():
#         setattr(current_user, field, value)

#     db.add(current_user)
#     await db.commit()
#     await db.refresh(current_user)
#     return current_user

# # ✅ Get all users (admin only)
# @router.get("/users", response_model=List[UserResponse], summary="Get all users (admin only)")
# async def get_all_users(
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     if current_user.role.upper() != "ADMIN":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can access this endpoint")

#     result = await db.execute(select(User))
#     users = result.scalars().all()
#     return users

# # ✅ Update user by ID (admin or owner)
# @router.put("/users/{user_id}", response_model=UserResponse, summary="Admin or user updates a user by ID")
# async def update_user(
#     user_id: int,
#     user_update: UserUpdate,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     result = await db.execute(select(User).where(User.id == user_id))
#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if current_user.role.upper() != "ADMIN" and current_user.id != user_id:
#         raise HTTPException(status_code=403, detail="Unauthorized")

#     for field, value in user_update.dict(exclude_unset=True).items():
#         setattr(user, field, value)

#     db.add(user)
#     await db.commit()
#     await db.refresh(user)
#     return user

# # ✅ Delete user by ID (admin or owner)
# @router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Admin or user deletes account")
# async def delete_user(
#     user_id: int,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     result = await db.execute(select(User).where(User.id == user_id))
#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if current_user.role.upper() != "ADMIN" and current_user.id != user_id:
#         raise HTTPException(status_code=403, detail="Unauthorized")

#     await db.delete(user)
#     await db.commit()




from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
from app.schemas.schema import (
    ForgotPasswordRequest, ResetPasswordRequest,
    UserCreate, UserResponse, Token, UserUpdate
)
from app.auth.auth import (
    get_db, register_user, login_for_access_token,
    request_password_reset, reset_password, get_current_user
)

router = APIRouter()

# Register new user
@router.post("/register", response_model=UserResponse, summary="Register a new user")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await register_user(user, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Registration error: {str(e)}")

# Login to get access token
@router.post("/login", response_model=Token, summary="Login for access token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        return await login_for_access_token(form_data, db)
    except ValueError as e:
        if "User not found" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found. Please register."
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed. Please check your credentials."
        )

# Request OTP for password reset
@router.post("/forgot-password", summary="Request OTP for password reset")
async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    try:
        await request_password_reset(data.email, db)
        return {"message": "OTP sent to your email"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found. Please check your email address."
        )

# Reset password with OTP
@router.post("/reset-password", summary="Reset password using OTP")
async def reset_password_route(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    try:
        await reset_password(data.email, data.otp, data.new_password, db)
        return {"message": "Password reset successful"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset failed. Please check your OTP and try again."
        )

# Get own profile
@router.get("/me", response_model=UserResponse, summary="Get current user profile")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# Update own profile
@router.put("/update-profile", response_model=UserResponse, summary="Update your own profile")
async def update_profile(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(current_user, field, value)

        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update profile: {str(e)}"
        )

# Get all users (admin only)
@router.get("/users", response_model=List[UserResponse], summary="Get all users (admin only)")
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this endpoint."
        )
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        )

# Update user by ID (admin or owner)
@router.put("/users/{user_id}", response_model=UserResponse, summary="Admin or user updates a user by ID")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        if current_user.role.upper() != "ADMIN" and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized to update this user."
            )

        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(user, field, value)

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update user: {str(e)}"
        )

# Delete user by ID (admin or owner)
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Admin or user deletes account")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        if current_user.role.upper() != "ADMIN" and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized to delete this user."
            )

        await db.delete(user)
        await db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete user: {str(e)}"
        )
