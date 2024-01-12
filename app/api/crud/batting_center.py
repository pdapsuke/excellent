from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import BattingCenter

def get_batting_center_by_id(session: Session, id: int):
    batting_center = session.query(BattingCenter).filter(BattingCenter.id == id).first()
    if batting_center is None:
        raise HTTPException(status_code=400, detail=f"batting_center with id:{id} not exists.")

    return batting_center
