from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class MachineInformationCreateSchema(BaseModel):
    ballspeed: List[int]
    pitch_type: List[str]
    batter_box: str
    username: str
    place_id: str


class MachineInformationConfigSchema(BaseModel):
    ballspeed: List[int]
    pitch_type: List[str]
    batter_box: str


class MachineInformationResponseSchema(BaseModel):
    id: int
    config: MachineInformationConfigSchema
    user_id: int
    batting_centers_id: int
    updated: datetime

    class Config:
        orm_mode = True
