
# from sqlalchemy import Column, Date, DateTime, Integer, String, Text, Float, ForeignKey, Enum, Boolean
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from app.database.connection import Base

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     password_hash = Column(String, nullable=True)
#     address = Column(Text)
#     phone = Column(String)

#     profile_image = Column(String, nullable=True)
#     gender = Column(String, nullable=True)
#     date_of_birth = Column(Date(), nullable=True)
#     is_active = Column(Boolean, default=True)
#     email_verified = Column(Boolean, default=False)
#     last_login = Column(DateTime, nullable=True)

#     google_id = Column(String, unique=True, nullable=True)
#     is_google_auth = Column(Boolean, default=False)
#     role = Column(String, default='customer')

#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     otp = Column(String, nullable=True)
#     otp_expires_at = Column(DateTime, nullable=True)

#     orders = relationship("Order", back_populates="user")
#     cart = relationship("Cart", back_populates="user")

# class Category(Base):
#     __tablename__ = 'categories'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     products = relationship("Product", back_populates="category")

# class Product(Base):
#     __tablename__ = 'products'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(Text)
#     price = Column(Float)
#     category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
#     stock = Column(Integer)
#     image_url = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     category = relationship("Category", back_populates="products")
#     order_items = relationship("OrderItem", back_populates="product")
#     cart_items = relationship("CartItem", back_populates="product")

# class Order(Base):
#     __tablename__ = 'orders'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
#     total_amount = Column(Float)
#     status = Column(String, default='pending', nullable=False)
#     shipping_address = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     user = relationship("User", back_populates="orders")
#     order_items = relationship("OrderItem", back_populates="order")
#     payment = relationship("Payment", back_populates="order", uselist=False)

# class OrderItem(Base):
#     __tablename__ = 'order_items'

#     id = Column(Integer, primary_key=True, index=True)
#     order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
#     product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
#     quantity = Column(Integer)
#     price = Column(Float)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     order = relationship("Order", back_populates="order_items")
#     product = relationship("Product", back_populates="order_items")
    

# class Cart(Base):
#     __tablename__ = 'carts'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     user = relationship("User", back_populates="cart")
#     cart_items = relationship("CartItem", back_populates="cart")

# class CartItem(Base):
#     __tablename__ = 'cart_items'

#     id = Column(Integer, primary_key=True, index=True)
#     cart_id = Column(Integer, ForeignKey('carts.id', ondelete='CASCADE'))
#     product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
#     quantity = Column(Integer)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     cart = relationship("Cart", back_populates="cart_items")
#     product = relationship("Product", back_populates="cart_items")

# # class Payment(Base):
# #     __tablename__ = 'payments'

# #     id = Column(Integer, primary_key=True, index=True)
# #     order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
# #     amount = Column(Float)
# #     payment_method = Column(String, nullable=False)
# #     status = Column(String, nullable=False)
# #     created_at = Column(DateTime, default=datetime.utcnow)
# #     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# #     order = relationship("Order", back_populates="payment")


# class Payment(Base):
#     __tablename__ = 'payments'

#     id = Column(Integer, primary_key=True, index=True)
#     order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
#     amount = Column(Float)
#     payment_method = Column(String, nullable=False)  # e.g. 'mpesa'
#     status = Column(String, nullable=False)          # e.g. 'pending', 'completed', 'failed'

#     # ✅ New Fields
#     phone_number = Column(String, nullable=True)     # For STK Push
#     mpesa_receipt_number = Column(String, nullable=True)  # Returned by Safaricom
#     transaction_date = Column(DateTime, nullable=True)     # Date of transaction from callback
#     merchant_request_id = Column(String, nullable=True)    # For reconciliation
#     checkout_request_id = Column(String, nullable=True)    # For tracking async callback

#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     order = relationship("Order", back_populates="payment")







from sqlalchemy import (
    Column, Date, DateTime, Integer, String, Text, Float, ForeignKey, Boolean, func
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True)
    address = Column(Text)
    phone = Column(String)

    profile_image = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    date_of_birth = Column(Date(), nullable=True)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)

    google_id = Column(String, unique=True, nullable=True)
    is_google_auth = Column(Boolean, default=False)
    role = Column(String, default='customer')

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    otp = Column(String, nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)

    orders = relationship("Order", back_populates="user")
    cart = relationship("Cart", back_populates="user")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    stock = Column(Integer)
    image_url = Column(String, nullable=True)  # Primary thumbnail (optional)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")

    images = relationship("ProductImage", back_populates="product", cascade="all, delete", passive_deletes=True)
    videos = relationship("ProductVideo", back_populates="product", cascade="all, delete", passive_deletes=True)


class ProductImage(Base):
    __tablename__ = 'product_images'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))

    product = relationship("Product", back_populates="images")


class ProductVideo(Base):
    __tablename__ = 'product_videos'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))

    product = relationship("Product", back_populates="videos")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    total_amount = Column(Float)
    status = Column(String, default='pending', nullable=False)
    shipping_address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
    quantity = Column(Integer)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="cart")
    cart_items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id', ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
    amount = Column(Float)
    payment_method = Column(String, nullable=False)
    status = Column(String, nullable=False, default="PENDING")  # PENDING, COMPLETED, CANCELLED, FAILED

    phone_number = Column(String, nullable=True)
    mpesa_receipt_number = Column(String, nullable=True)
    transaction_date = Column(DateTime, nullable=True)
    merchant_request_id = Column(String, nullable=True)
    checkout_request_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=func.utcnow())
    updated_at = Column(DateTime, default=func.utcnow(), onupdate=func.utcnow())

    order = relationship("Order", back_populates="payment")