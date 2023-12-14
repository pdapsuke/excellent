from typing import Optional, List
from pydantic import BaseModel

from schema.machine import MachineInformationResponseSchema

class BattingCenterGetSchema(BaseModel):
    prefecture_city: str
    username: str

class BattingCenterResponseSchema(BaseModel):
    id: int
    place_id: str
    name: str
    formatted_address: str
    photos: Optional[List]
    itta_count: int
    itta: str # 行った！フラグ

class BattingCenterIttaUpdateSchema(BaseModel):
    id: int
    itta_count: int
    itta: str # 行った！フラグ
