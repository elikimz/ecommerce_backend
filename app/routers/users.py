from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schema import ForgotPasswordRequest, ResetPasswordRequest, UserCreate, UserResponse, Token
from app.auth.auth import get_db, register_user, login_for_access_token, request_password_reset, reset_password

router = APIRouter()

# ✅ Add OAuth2 scheme (this makes the "Authorize" button appear)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ✅ Dummy function to simulate getting current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": "testuser"}  # Replace with real user lookup

@router.post("/register", response_model=UserResponse, summary="Register a new user")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user(user, db)

@router.post("/login", response_model=Token, summary="Login for access token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await login_for_access_token(form_data, db)

# @router.get('/login/google', summary="Login with Google")
# async def login_google_route(request: Request):
#     return await login_google(request)

# @router.get('/auth/google', name='auth_google', summary="Authenticate with Google")
# async def auth_google_route(request: Request, db: AsyncSession = Depends(get_db)):
#     return await auth_google(request, db)

# ✅ Protected route to trigger the Authorize button and test token
@router.get("/protected", summary="Protected route (requires token)")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}! You're authenticated."}



@router.post("/forgot-password", summary="Request OTP for password reset")
async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    await request_password_reset(data.email, db)
    return {"message": "OTP sent to your email"}

@router.post("/reset-password", summary="Reset password using OTP")
async def reset_password_route(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    await reset_password(data.email, data.otp, data.new_password, db)
    return {"message": "Password reset successful"}