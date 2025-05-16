from fastapi import APIRouter, FastAPI

from app.user.router import user_router

app = FastAPI()

routers: list[APIRouter] = [user_router]

for router in routers:
    app.include_router(router)
