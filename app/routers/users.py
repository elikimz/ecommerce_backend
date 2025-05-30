# from typing import List
# from fastapi import APIRouter, Depends, Request, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.models.models import User
# from app.schemas.schema import ForgotPasswordRequest, ResetPasswordRequest, UserCreate, UserResponse, Token, UserUpdate
# from app.auth.auth import get_db, register_user, login_for_access_token, request_password_reset, reset_password
# from app.auth.auth import get_current_user


# router = APIRouter()

# # ✅ Add OAuth2 scheme (this makes the "Authorize" button appear)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



# @router.post("/register", response_model=UserResponse, summary="Register a new user")
# async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     return await register_user(user, db)

# @router.post("/login", response_model=Token, summary="Login for access token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
#     return await login_for_access_token(form_data, db)

# # @router.get('/login/google', summary="Login with Google")
# # async def login_google_route(request: Request):
# #     return await login_google(request)

# # @router.get('/auth/google', name='auth_google', summary="Authenticate with Google")
# # async def auth_google_route(request: Request, db: AsyncSession = Depends(get_db)):
# #     return await auth_google(request, db)

# # ✅ Protected route to trigger the Authorize button and test token
# @router.get("/protected", summary="Protected route (requires token)")
# async def protected_route(current_user: dict = Depends(get_current_user)):
#     return {"message": f"Hello, {current_user['username']}! You're authenticated."}



# @router.post("/forgot-password", summary="Request OTP for password reset")
# async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
#     await request_password_reset(data.email, db)
#     return {"message": "OTP sent to your email"}

# @router.post("/reset-password", summary="Reset password using OTP")
# async def reset_password_route(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
#     await reset_password(data.email, data.otp, data.new_password, db)
#     return {"message": "Password reset successful"}


# @router.put("/update-profile", summary="Update user profile", response_model=UserResponse)
# async def update_profile(
#     user_update: UserUpdate,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user)  # Use the real function that returns User model
# ):
#     if user_update.address is not None:
#         current_user.address = user_update.address
#     if user_update.phone is not None:
#         current_user.phone = user_update.phone

#     db.add(current_user)
#     await db.commit()
#     await db.refresh(current_user)

#     return current_user


# @router.get("/users", response_model=List[UserResponse])
# async def get_all_users(
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     print("CURRENT USER:", current_user)
#     print("ROLE:", current_user.role)

#     if current_user.role.upper() != "ADMIN":
#      raise HTTPException(
#          status_code=status.HTTP_403_FORBIDDEN,
#         detail="Only admins can access this endpoint"
#     )
#     result = await db.execute(select(User))
#     users = result.scalars().all()
#     return users


from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User
from app.schemas.schema import ForgotPasswordRequest, ResetPasswordRequest, UserCreate, UserResponse, Token, UserUpdate
from app.auth.auth import get_db, register_user, login_for_access_token, request_password_reset, reset_password
from app.auth.auth import get_current_user

router = APIRouter()

# ✅ Register new user
@router.post("/register", response_model=UserResponse, summary="Register a new user")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user(user, db)

# ✅ Login to get access token
@router.post("/login", response_model=Token, summary="Login for access token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await login_for_access_token(form_data, db)

# ✅ Request OTP for password reset
@router.post("/forgot-password", summary="Request OTP for password reset")
async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    await request_password_reset(data.email, db)
    return {"message": "OTP sent to your email"}

# ✅ Reset password with OTP
@router.post("/reset-password", summary="Reset password using OTP")
async def reset_password_route(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    await reset_password(data.email, data.otp, data.new_password, db)
    return {"message": "Password reset successful"}

# ✅ Update own profile
@router.put("/update-profile", response_model=UserResponse, summary="Update user profile")
async def update_profile(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_update.address is not None:
        current_user.address = user_update.address
    if user_update.phone is not None:
        current_user.phone = user_update.phone

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user

# ✅ Get all users (admin only)
@router.get("/users", response_model=List[UserResponse], summary="Get all users (admin only)")
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can access this endpoint")

    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

# ✅ Update user by id (admin or owner)
@router.put("/users/{user_id}", response_model=UserResponse, summary="Admin or user updates their account")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if current user is admin or updating their own profile
    if current_user.role.upper() != "ADMIN" and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")

    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.address is not None:
        user.address = user_update.address
    if user_update.phone is not None:
        user.phone = user_update.phone

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

# ✅ Delete user by id (admin or owner)
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Admin or user deletes their account")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if current user is admin or deleting their own profile
    if current_user.role.upper() != "ADMIN" and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")

    await db.delete(user)
    await db.commit()

    return  # 204 No Content
