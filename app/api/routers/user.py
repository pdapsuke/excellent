from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_cloudauth.cognito import CognitoClaims
from fastapi.responses import JSONResponse
import requests
from sqlalchemy.orm import Session

from auth import get_current_user
from crud import user as crud_user
from env import Environment
from models import User
from schema.batting_center import (
    BattingCenterMypageResponseSchema,
    BattingCenterResponseSchema,
)
from session import get_session
from utils import logger

router = APIRouter()
env = Environment()

@router.post("/users/signin")
def signin_user(
    session: Session = Depends(get_session),
    user: CognitoClaims = Depends(get_current_user)
):
    # userがDBに登録済みか、メールアドレスで検索
    current_user = session.query(User).filter(User.email == user.email).first()

    # userがDBに未登録の場合、新規登録
    if current_user is None:
        user = User(
            username = user.username,
            email = user.email,
        )
        session.add(user)
        session.commit()
        logger.info(f"new user created id: {user.id}, email: {user.email}")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "user created."})

    return JSONResponse(status_code=200, content={"message": "user already exists."})

# 現在のユーザーが行った！したバッティングセンターの取得
@router.get("/users/me/itta_centers", response_model=List[BattingCenterResponseSchema])
def get_itta_centers(
    session: Session = Depends(get_session),
    user: CognitoClaims = Depends(get_current_user)
):
    current_user = crud_user.get_user_by_email(session=session, email=user.email)

    itta_batting_centers = current_user.itta_centers # 行った！済みのバッティングセンターを取得
    result_list: List[BattingCenterResponseSchema] = [] # バッティングセンターのレスポンスを格納するリストを定義

    # 行った！済みのバッティングセンターについて、情報を設定し、オブジェクトをレスポンス用リストに追加
    for itta_batting_center in itta_batting_centers:

        # Google PlaceDetails APIへ施設名、住所、写真をリクエスト
        payload = {"place_id": itta_batting_center.place_id, "language": "ja", "fiels": "name,formatted_address,photos", "key": env.find_place_api_key}
        response = requests.get(env.place_details_url, params=payload).json()["result"]
        result_list.append(BattingCenterResponseSchema(
            id = itta_batting_center.id,
            place_id = itta_batting_center.place_id,
            name = response["name"],
            formatted_address = response["formatted_address"].split("、", 1)[-1], # "日本、"という文字列が先頭につくため加工する
            photos = response["photos"] if "photos" in response else None,
            itta_count = itta_batting_center.count_itta(),
            itta = itta_batting_center.set_itta_flag(current_user),
        ))

    return result_list

# 現在のユーザーが投稿したマシン情報と紐づくバッティングセンターの情報を取得
@router.get("/users/me/posted_machine_informations", response_model=List[BattingCenterMypageResponseSchema])
def get_posted_machine_informations(
    session: Session = Depends(get_session),
    user: CognitoClaims = Depends(get_current_user)
):
    current_user = crud_user.get_user_by_email(session=session, email=user.email)
    posted_machine_informations = current_user.machine_informations # 投稿したマシン情報を取得
    if len(posted_machine_informations) == 0:
        return []

    result_list = crud_user.create_mypage_response(current_user=current_user, target_machine_informations=posted_machine_informations)

    return result_list

# 現在のユーザーがなかった！したマシン情報と紐づくバッティングセンターの情報を取得
@router.get("/users/me/nakatta_machine_informations", response_model=List[BattingCenterMypageResponseSchema])
def get_nakatta_machine_informations(
    session: Session = Depends(get_session),
    user: CognitoClaims = Depends(get_current_user)
):
    current_user = crud_user.get_user_by_email(session=session, email=user.email)
    nakatta_machine_informations = current_user.nakatta_machines # なかった！したマシン情報を取得
    if len(nakatta_machine_informations) == 0:
        return []

    result_list = crud_user.create_mypage_response(current_user=current_user, target_machine_informations=nakatta_machine_informations)

    return result_list

# 現在のユーザーがあった！したマシン情報と紐づくバッティングセンターの情報を取得
@router.get("/users/me/atta_machine_informations", response_model=List[BattingCenterMypageResponseSchema])
def get_atta_machine_informations(
    session: Session = Depends(get_session),
    user: CognitoClaims = Depends(get_current_user)
):
    current_user = crud_user.get_user_by_email(session=session, email=user.email)
    atta_machine_informations = current_user.atta_machines # あった！したマシン情報を取得
    if len(atta_machine_informations) == 0:
        return []

    result_list = crud_user.create_mypage_response(current_user=current_user, target_machine_informations=atta_machine_informations)

    return result_list
