import json
from typing import List, Optional

import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends, HTTPException
from schema.batting_center import (
    BattingCenterGetSchema,
    BattingCenterResponseSchema,
)

from models import IttaUsersCenters, BattingCenter, User, MachineInformation, AttaUserMachine, NakattaUserMachine
from session import get_session

router = APIRouter()

# Find Place
@router.post("/batting_centers/")
def get_batting_centers(
    data: BattingCenterGetSchema,
    session: Session = Depends(get_session),
):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    payload = {"query": f"{data.prefecture_city} バッティングセンター","language": "ja", "key": "***REMOVED***"}
    # usernameから現在のユーザーを取得
    current_user = session.query(User).filter(User.username == data.username).first()
    batting_centers = requests.get(url, params=payload).json()["results"]
    for batting_center in batting_centers:
        
        place_id = batting_center["place_id"]
        registered_batting_center = session.query(BattingCenter).filter(BattingCenter.place_id == place_id).first()

        # 初めて取得したバッティングセンターはDBに登録
        if registered_batting_center is None:
            new_batting_center = BattingCenter(place_id = place_id)
            session.add(new_batting_center)
            session.commit()
            # 行った！フラグをfalseに設定
            batting_center["itta"] = "no"
        else:
            if registered_batting_center in current_user.itta_centers:
                # 行った！フラグをtrueに設定
                batting_center["itta"] = "yes"
            else:
                batting_center["itta"] = "no"

    return batting_centers

# DBにあるバッティングセンターをすべて取得
@router.get("/batting_centers/")
def get_batting_centers(
    session: Session = Depends(get_session),
):
    batting_centers = session.query(BattingCenter).all()

    return batting_centers

# place_idごとの行った数
@router.get("/batting_centers/itta/{place_id}")
def read_itta_count(
    place_id: str,
    session: Session = Depends(get_session),
):
    batting_center = session.query(BattingCenter).filter(BattingCenter.place_id == place_id).first()
    itta_count = session.query(IttaUsersCenters).filter(IttaUsersCenters.batting_center_id == batting_center.id).count()

    return {"count": itta_count}

# place_idでバッティングセンターの詳細情報を取得
@router.get("/batting_centers/{place_id}")
def get_batting_center(
    username: str,
    place_id: str,
    session: Session = Depends(get_session),
):
    user = session.query(User).filter(User.username == username).first()
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    payload = {"place_id": place_id, "language": "ja", "key": "***REMOVED***"}
    batting_center_name = requests.get(url, params=payload).json()["result"]["name"]
    batting_center = session.query(BattingCenter).filter(BattingCenter.place_id == place_id).first()
    batting_center.name = batting_center_name
    

    for machine_information in batting_center.machine_informations:
        if machine_information in user.atta_machines:
            machine_information.atta = "yes"
            machine_information.nakatta = "no"
        elif machine_information in user.nakatta_machines:
            machine_information.atta = "no"
            machine_information.nakatta = "yes"
        else:
            machine_information.atta = "no"
            machine_information.nakatta = "no"

    for machine_information in batting_center.machine_informations:
        atta_count = session.query(AttaUserMachine).filter(AttaUserMachine.machine_info_id == machine_information.id).count()
        nakatta_count = session.query(NakattaUserMachine).filter(NakattaUserMachine.machine_info_id == machine_information.id).count()
        machine_information.atta_count = atta_count
        machine_information.nakatta_count = nakatta_count

    for machine_information in batting_center.machine_informations:
        machine_information.config = json.loads(machine_information.config)

    return batting_center