from typing import List

import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends, HTTPException
from schema.batting_center import (
    BattingCenterGetSchema,
    BattingCenterResponseSchema,
)

from models import IttaUsersCenters, BattingCenter
from session import get_session

router = APIRouter()

# Find Place
@router.post("/batting_centers/")
def get_batting_centers(
    data: BattingCenterGetSchema
):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    payload = {"query": f"{data.prefecture_city} バッティングセンター","language": "ja", "key": "***REMOVED***"}
    response = requests.get(url, params=payload)
    return response.json()["results"]

# DBにあるバッティングセンターをすべて取得
@router.get("/batting_centers/", response_model=List[BattingCenterResponseSchema])
def get_batting_centers(
    session: Session = Depends(get_session),
):
    batting_centers = session.query(BattingCenter).all()

    return batting_centers

# place_idごとの行った数
@router.get("/batting_centers/itta/{place_id}")
def read_itta_count(
    place_id: int,
    session: Session = Depends(get_session),
):
    batting_center = session.query(BattingCenter).filter(BattingCenter.place_id == place_id).first()
    itta_count = session.query(IttaUsersCenters).filter(IttaUsersCenters.batting_center_id == batting_center.id).count()

    return {"count": itta_count}