from datetime import datetime
from typing import Optional, List
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
    breaking_balls: List[BreakingBallResponseSchema]
    ball_speeds: List[BallSpeedResponseSchema]
    updated: datetime

    class Config:
        orm_mode = True
