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
    photos: Optional[str]
    itta_count: int
    itta: bool

class BattingCenterDetailResponseSchema(BaseModel):
    id: int
    place_id: str
    name: str
    formatted_address: str
    photos: List[str]
    itta_count: int
    itta: bool
    machine_informations: List[MachineInformationResponseSchema]

# 投稿、あった！、なかった！したマシン情報を返す
class BattingCenterMypageResponseSchema(BaseModel):
    id: int
    place_id: str
    name: str
    formatted_address: str
    machine_informations: List[MachineInformationResponseSchema]

# 行った！したバッティングセンターを返す ＊画像情報は返さない
class IttaBattingCenterResponseSchema(BaseModel):
    id: int
    place_id: str
    name: str
    formatted_address: str
    itta_count: int
    itta: bool

class BattingCenterIttaUpdateSchema(BaseModel):
    id: int
    itta_count: int
    itta: bool
