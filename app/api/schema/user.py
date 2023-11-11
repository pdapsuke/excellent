from typing import Optional, List
from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    jwt_token: str

class UserResponseSchema(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True
    
