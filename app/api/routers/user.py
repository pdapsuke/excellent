from typing import List
import json
import base64

from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends, HTTPException

from models import User, BattingCenter
from session import get_session
from schema.user import (
    UserLoginSchema,
    UserResponseSchema,
    UpdateIttaSchema,
)

router = APIRouter()

@router.post("/users/", response_model=UserResponseSchema)
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
        return user

    return current_user

# ユーザー一覧
@router.get("/users/", response_model=List[UserResponseSchema])
def read_users(
    skip: int = 0,  # GETパラメータ
    limit: int = 100,  # GETパラメータ
    session: Session = Depends(get_session),
):
    users = session.query(User).offset(skip).limit(limit).all()
    return users

# 行った！の更新
@router.put("/users/me/itta", response_model=UserResponseSchema)
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
        return user
    elif data.itta == "no":
        # 既に行った！したバッティングセンターを削除
        current_itta_centers = user.itta_centers
        new_itta_centers = list(filter(lambda x: x.place_id != data.place_id, current_itta_centers))
        user.itta_centers = new_itta_centers
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    else:
        raise HTTPException(status_code=400, detail="bad request")
