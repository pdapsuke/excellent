from fastapi import FastAPI
from api.routers import (
    prefecture_city,
    batting_center,
    user,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(prefecture_city.router, prefix="/api/v1")
app.include_router(batting_center.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)