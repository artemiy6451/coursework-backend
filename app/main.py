from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.user.router import user_router

app = FastAPI()

origins = ["https://192.168.0.108:5173", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers: list[APIRouter] = [user_router]

for router in routers:
    app.include_router(router)
