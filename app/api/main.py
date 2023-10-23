from fastapi import FastAPI
from api.routers import (
    batting_center,
    user,
)

app = FastAPI()

app.include_router(router, prefix="/api/v1")