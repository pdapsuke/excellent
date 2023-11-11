from typing import List
import json
import base64

from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends

from models import User
from session import get_session
from schema.user import (
    UserLoginSchema,
    UserResponseSchema,
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
