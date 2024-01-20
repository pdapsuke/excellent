from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from env import Environment
from models import (
    BallSpeed,
    BreakingBall,
)
from schema.machine import (
    BallSpeedResponseSchema,
    BreakingBallResponseSchema,
)
from session import get_session

router = APIRouter()
env = Environment()

# 球種一覧を取得
@router.get("/machine_configurations/breaking_balls", response_model=List[BreakingBallResponseSchema])
def get_breaking_balls(
    session: Session = Depends(get_session),
):
    breaking_balls = session.query(BreakingBall).all()

    return breaking_balls

# 球種一覧を取得
@router.get("/machine_configurations/ball_speeds", response_model=List[BallSpeedResponseSchema])
def get_ball_speeds(
    session: Session = Depends(get_session),
):
    ball_speeds = session.query(BallSpeed).all()

    return ball_speeds
