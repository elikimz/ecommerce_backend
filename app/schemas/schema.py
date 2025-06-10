
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional
from datetime import date, datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    id:int

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    address: str
    phone: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: str
    phone: str
    profile_image: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)





class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None





class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    stock: int
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: CategoryOut

    class Config:
        orm_mode = True


# --- OrderItem ---
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        orm_mode = True

# --- Order ---
class OrderBase(BaseModel):
    total_amount: float
    shipping_address: str
    status: Optional[str] = "pending"

class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    total_amount: Optional[float] = None
    shipping_address: Optional[str] = None
    status: Optional[str] = None

class OrderOut(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItemOut]

    class Config:
        orm_mode = True        


class CartItemOut(BaseModel):
    product_id: int
    quantity: int
    product: Optional[ProductOut]

    class Config:
        orm_mode = True

class CartOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    cart_items: Optional[List[CartItemOut]] = []

    class Config:
        orm_mode = True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int
    

class CartItemUpdate(BaseModel):
    product_id: int
    quantity: int