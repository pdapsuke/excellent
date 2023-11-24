from typing import List
import json
import base64

from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends, HTTPException

from models import User, BattingCenter, MachineInformation
from session import get_session
from schema.user import (
    UserLoginSchema,
    UserResponseSchema,
    UpdateIttaSchema,
    UpdateAttaNakattaSchema,
)

router = APIRouter()

@router.post("/users/")
def login_user(
    data: UserLoginSchema,
    session: Session = Depends(get_session),
):
    payload = data.jwt_token.split(".")[1]

    # Base64デコード
    decoded_payload = base64.urlsafe_b64decode(payload + '=' * (4 - len(payload) % 4)).decode()

    # JSONデコード
    json_payload = json.loads(decoded_payload)

    # return json_payload

    current_user = session.query(User).filter(User.username == json_payload["cognito:username"]).first()

    if current_user is None:
        user = User(
            username = json_payload["cognito:username"],
            email = json_payload["email"],
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status": 200}

    return {"status": 200}

# ユーザー一覧
@router.get("/users/")
def read_users(
    skip: int = 0,  # GETパラメータ
    limit: int = 100,  # GETパラメータ
    session: Session = Depends(get_session),
):
    users = session.query(User).offset(skip).limit(limit).all()
    return users

# ユーザー詳細
@router.get("/users/{id}")
def read_user(
    id: int,
    session: Session = Depends(get_session),
):
    user = session.query(User).filter(User.id == id).first()
    itta_batting_centers = user.itta_centers
    atta_machines = user.atta_machines
    nakatta_machines = user.nakatta_machines

    return user

# 行った！の更新
@router.put("/users/me/itta")
def update_itta(
    data: UpdateIttaSchema,
    session: Session = Depends(get_session),
):
    user = session.query(User).filter(User.username == data.username).first()
    if user is None:
        raise HTTPException(status_code=400, detail=f"{data.username} not exists.")

    batting_center = session.query(BattingCenter).filter(BattingCenter.place_id == data.place_id).first()

    if data.itta == "yes":
        # 行った！したバッティングセンターを新規追加
        itta_centers = user.itta_centers
        itta_centers.append(batting_center)
        
        user.itta_centers = itta_centers
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status": 200}
    elif data.itta == "no":
        # 既に行った！したバッティングセンターを削除
        current_itta_centers = user.itta_centers
        new_itta_centers = list(filter(lambda x: x.place_id != data.place_id, current_itta_centers))
        user.itta_centers = new_itta_centers
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status": 200}
    else:
        raise HTTPException(status_code=400, detail="bad request")

# あった！なかった！の更新
@router.put("/users/me/atta_nakatta")
def update_atta_nakatta(
    data: UpdateAttaNakattaSchema,
    session: Session = Depends(get_session),
):
    user = session.query(User).filter(User.username == data.username).first()
    if user is None:
        raise HTTPException(status_code=400, detail=f"{data.username} not exists.")

    target_machine = session.query(MachineInformation).filter(MachineInformation.id == data.machine_id).first()
    if target_machine is None:
        raise HTTPException(status_code=400, detail=f"machine_id: {data.machine_id} not exists.")

    # あった！なかった！の新規追加
    if data.add_atta_nakatta == "yes":

        if data.atta_nakatta == "atta":
            # あった！したマシン情報を新規追加
            atta_machines = user.atta_machines
            atta_machines.append(target_machine)
            session.add(user)
            session.commit()
            session.refresh(user)

            # 既になかった！したマシン情報があれば削除
            if target_machine in user.nakatta_machines:
                current_nakatta_machines = user.nakatta_machines
                new_nakatta_machines = list(filter(lambda x: x.id != data.machine_id, current_nakatta_machines))

                user.nakatta_machines = new_nakatta_machines
                session.add(user)
                session.commit()
                session.refresh(user)
            
            return {"status": 200}

        elif data.atta_nakatta == "nakatta":
            # なかった！したマシン情報を新規追加
            nakatta_machines = user.nakatta_machines
            nakatta_machines.append(target_machine)
            session.add(user)
            session.commit()
            session.refresh(user)
            
            # 既にあった！したマシン情報があれば削除
            if target_machine in user.atta_machines:
                current_atta_machines = user.atta_machines
                new_atta_machines = list(filter(lambda x: x.id != data.machine_id, current_atta_machines))

                user.atta_machines = new_atta_machines
                session.add(user)
                session.commit()
                session.refresh(user)
            
            return {"status": 200}

        else:
            raise HTTPException(status_code=400, detail="bad request")

    # あった！なかった！の削除
    if data.add_atta_nakatta == "no":

        if data.atta_nakatta == "atta":
            # あった！したマシン情報を削除
            current_atta_machines = user.atta_machines
            new_atta_machines = list(filter(lambda x: x.id != data.machine_id, current_atta_machines))

            user.atta_machines = new_atta_machines
            session.add(user)
            session.commit()
            session.refresh(user)
        
            return {"status": 200}

        elif data.atta_nakatta == "nakatta":
            # なかった！したマシン情報を削除
            current_nakatta_machines = user.nakatta_machines
            new_nakatta_machines = list(filter(lambda x: x.id != data.machine_id, current_nakatta_machines))

            user.nakatta_machines = new_nakatta_machines
            session.add(user)
            session.commit()
            session.refresh(user)
        
            return {"status": 200}

        else:
            raise HTTPException(status_code=400, detail="bad request")

    else:
        raise HTTPException(status_code=400, detail="bad request")
