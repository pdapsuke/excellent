from typing import Optional, List
from pydantic import BaseModel

class BattingCenterGetSchema(BaseModel):
    prefecture_city: str

class BattingCenterResponseSchema(BaseModel):
    place_id: str

    class Config:
        orm_mode = True

