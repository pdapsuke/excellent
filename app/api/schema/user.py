from typing import Optional, List
from typing import List

from pydantic import BaseModel

from schema.batting_center import BattingCenterResponseSchema

class UserLoginSchema(BaseModel):
    jwt_token: str

class UserResponseSchema(BaseModel):
    username: str
    email: str
    itta_centers: List[BattingCenterResponseSchema]

    class Config:
        orm_mode = True
    
class UpdateIttaSchema(BaseModel):
    username: str
    place_id: int
