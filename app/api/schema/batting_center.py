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

class BattingCenterDetailResponseSchema(BaseModel):
    id: int
    place_id: str
    name: str
    formatted_address: str
    photos: Optional[List]
    itta_count: int
    itta: str # 行った！フラグ
    machine_informations: List[MachineInformationResponseSchema]

# 投稿、あった！、なかった！したマシン情報を返す
class BattingCenterMypageResponseSchema(BaseModel):
    id: int
    place_id: str
    name: str
    formatted_address: str
    machine_informations: List[MachineInformationResponseSchema]

class BattingCenterIttaUpdateSchema(BaseModel):
    id: int
    itta_count: int
    itta: str # 行った！フラグ
