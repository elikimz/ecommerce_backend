from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routers import users ,categories,products,order,cart,cart_items

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="super-secret-session-key-please-change")

# Include routers
app.include_router(users.router, tags=["auth"]),
app.include_router(categories.router, tags=["Category"]),
app.include_router(products.router,  prefix="/products",tags=["Products"]),
app.include_router(order.router, prefix="/orders", tags=["order"]),
app.include_router(cart.router, prefix="/cart", tags=["Cart"]),
app.include_router(cart_items.router, tags=["CartItems"])


@app.get("/")
def root():
    return {"message": "Ecommerce API is running"}
