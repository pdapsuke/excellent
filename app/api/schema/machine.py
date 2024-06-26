from datetime import datetime
from typing import List

from pydantic import BaseModel

class BreakingBallResponseSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BallSpeedResponseSchema(BaseModel):
    id: int
    speed: int

    class Config:
        orm_mode = True


class MachineInformationCreateUpdateSchema(BaseModel):
    ballspeed_ids: List[int]
    breaking_ball_ids: List[int]
    batter_box: str


class MachineInformationResponseSchema(BaseModel):
    id: int
    is_owner: bool
    breaking_balls: List[BreakingBallResponseSchema]
    ball_speeds: List[BallSpeedResponseSchema]
    batter_box: str
    atta_count: int
    atta: bool
    nakatta_count: int
    nakatta: bool
    updated: datetime


class MachineInformationUpdateAttaNakattaResponseSchema(BaseModel):
    id: int
    atta_count: int
    nakatta_count: int
    atta: bool
    nakatta: bool
