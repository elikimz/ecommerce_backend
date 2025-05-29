from fastapi import FastAPI
from app.routers import users
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()



app.add_middleware(SessionMiddleware, secret_key="super-secret-session-key-please-change")

app.include_router(users.router, tags=["auth"])


@app.get("/")
def root():
    return {"message": "Ecommerce API is running"}

