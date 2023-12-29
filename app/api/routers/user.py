from typing import List

import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_cloudauth.cognito import CognitoClaims

from models import User
from session import get_session
from schema.batting_center import (
    BattingCenterResponseSchema,
    BattingCenterMypageResponseSchema,
)
from schema.machine import (
    MachineInformationResponseSchema,
    BreakingBallResponseSchema,
    BallSpeedResponseSchema,
)
from auth import get_current_user
from env import Environment
from utils import logger

router = APIRouter()
env = Environment()

@router.post("/users/signin")
def signin_user(
    session: Session = Depends(get_session),
    current_user: CognitoClaims = Depends(get_current_user)
):
    # current_userがDBに登録済みか、メールアドレスで検索
    registared_user = session.query(User).filter(User.email == current_user.email).first()

    # current_userがDBに未登録の場合、新規登録
    if registared_user is None:
        user = User(
            username = current_user.username,
            email = current_user.email,
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
    # DBに登録済みのユーザーを取得、見つからなければ400エラー
    current_user = session.query(User).filter(User.email == user.email).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail=f"{current_user.username} not exists.")

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
    # DBに登録済みのユーザーを取得、見つからなければ400エラー
    current_user = session.query(User).filter(User.email == user.email).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail=f"{current_user.username} not exists.")

    posted_machine_informations = current_user.machine_informations # 投稿したマシン情報を取得
    result_list: List[BattingCenterMypageResponseSchema] = [] # レスポンス（投稿したマシン情報と紐づくバッティングセンター）を格納するリスト

    # 投稿したマシン情報に関連するバッティングセンターを取得
    related_batting_centers = set([posted.batting_center for posted in posted_machine_informations])

    # 関連するバッティングセンターごとにオブジェクトを作成し、レスポンス格納リストに追加していく
    for related_batting_center in related_batting_centers:

        # Google PlaceDetails APIへ施設名と住所をリクエスト
        payload = {"place_id": related_batting_center.place_id, "language": "ja", "fields": "name,formatted_address", "key": env.find_place_api_key}
        response = requests.get(env.place_details_url, params=payload).json()["result"]

        # バッティングセンターに関連するマシン情報のみをフィルタ
        filtered_posted_machine_informations = list(filter(lambda x: x.batting_center == related_batting_center, posted_machine_informations))
        machine_information_responses: List[MachineInformationResponseSchema] = [] # マシン情報のレスポンスを格納するリストを定義

        # マシン情報のレスポンスに必要な情報を設定し、オブジェクトをレスポンス用リストに追加
        for machine_information in filtered_posted_machine_informations:
            breaking_balls = [BreakingBallResponseSchema(id = bb.id, name = bb.name) for bb in machine_information.breaking_balls]
            ball_speeds = [BallSpeedResponseSchema(id = bs.id, speed = bs.speed) for bs in machine_information.ball_speeds]
            machine_information_responses.append(MachineInformationResponseSchema(
                id = machine_information.id,
                user_id = machine_information.user_id,
                breaking_balls = breaking_balls,
                ball_speeds = ball_speeds,
                atta_count = machine_information.count_atta(),
                nakatta_count = machine_information.count_nakatta(),
                atta = machine_information.set_atta_flag(current_user),
                nakatta = machine_information.set_nakatta_flag(current_user),
                updated = machine_information.updated
            ))
        result_list.append(BattingCenterMypageResponseSchema(
            id = related_batting_center.id,
            place_id = related_batting_center.place_id,
            name = response["name"],
            formatted_address = response["formatted_address"].split("、", 1)[-1], # "日本、"という文字列が先頭につくため加工する
            machine_informations = machine_information_responses
        ))

    return result_list

# 現在のユーザーがなかった！したマシン情報と紐づくバッティングセンターの情報を取得
@router.get("/users/me/nakatta_machine_informations", response_model=List[BattingCenterMypageResponseSchema])
def get_nakatta_machine_informations(
    session: Session = Depends(get_session),
    user: CognitoClaims = Depends(get_current_user)
):
    # DBに登録済みのユーザーを取得、見つからなければ400エラー
    current_user = session.query(User).filter(User.email == user.email).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail=f"{current_user.username} not exists.")

    nakatta_machine_informations = current_user.nakatta_machines # あった！したマシン情報を取得
    result_list: List[BattingCenterMypageResponseSchema] = [] # レスポンス（あった！したマシン情報と紐づくバッティングセンター）を格納するリスト

    # あった！したマシン情報に関連するバッティングセンターを取得
    related_batting_centers = set([nakatta.batting_center for nakatta in nakatta_machine_informations])

    # 関連するバッティングセンターごとにオブジェクトを作成し、レスポンス格納リストに追加していく
    for related_batting_center in related_batting_centers:

        # Google PlaceDetails APIへ施設名と住所をリクエスト
        payload = {"place_id": related_batting_center.place_id, "language": "ja", "fields": "name,formatted_address", "key": env.find_place_api_key}
        response = requests.get(env.place_details_url, params=payload).json()["result"]

        # バッティングセンターに関連するマシン情報のみをフィルタ
        filtered_nakatta_machine_informations = list(filter(lambda x: x.batting_center == related_batting_center, nakatta_machine_informations))
        machine_information_responses: List[MachineInformationResponseSchema] = [] # マシン情報のレスポンスを格納するリストを定義

        # マシン情報のレスポンスに必要な情報を設定し、オブジェクトをレスポンス用リストに追加
        for machine_information in filtered_nakatta_machine_informations:
            breaking_balls = [BreakingBallResponseSchema(id = bb.id, name = bb.name) for bb in machine_information.breaking_balls]
            ball_speeds = [BallSpeedResponseSchema(id = bs.id, speed = bs.speed) for bs in machine_information.ball_speeds]
            machine_information_responses.append(MachineInformationResponseSchema(
                id = machine_information.id,
                user_id = machine_information.user_id,
                breaking_balls = breaking_balls,
                ball_speeds = ball_speeds,
                atta_count = machine_information.count_atta(),
                nakatta_count = machine_information.count_nakatta(),
                atta = machine_information.set_atta_flag(current_user),
                nakatta = machine_information.set_nakatta_flag(current_user),
                updated = machine_information.updated
            ))
        result_list.append(BattingCenterMypageResponseSchema(
            id = related_batting_center.id,
            place_id = related_batting_center.place_id,
            name = response["name"],
            formatted_address = response["formatted_address"].split("、", 1)[-1], # "日本、"という文字列が先頭につくため加工する
            machine_informations = machine_information_responses
        ))

    return result_list

# 現在のユーザーがあった！したマシン情報と紐づくバッティングセンターの情報を取得
@router.get("/users/me/atta_machine_informations", response_model=List[BattingCenterMypageResponseSchema])
def get_atta_machine_informations(
    session: Session = Depends(get_session),
    user: CognitoClaims = Depends(get_current_user)
):
    # DBに登録済みのユーザーを取得、見つからなければ400エラー
    current_user = session.query(User).filter(User.email == user.email).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail=f"{current_user.username} not exists.")

    atta_machine_informations = current_user.atta_machines # あった！したマシン情報を取得
    result_list: List[BattingCenterMypageResponseSchema] = [] # レスポンス（あった！したマシン情報と紐づくバッティングセンター）を格納するリスト

    # あった！したマシン情報に関連するバッティングセンターを取得
    related_batting_centers = set([atta.batting_center for atta in atta_machine_informations])

    # 関連するバッティングセンターごとにオブジェクトを作成し、レスポンス格納リストに追加していく
    for related_batting_center in related_batting_centers:

        # Google PlaceDetails APIへ施設名と住所をリクエスト
        payload = {"place_id": related_batting_center.place_id, "language": "ja", "fields": "name,formatted_address", "key": env.find_place_api_key}
        response = requests.get(env.place_details_url, params=payload).json()["result"]

        # バッティングセンターに関連するマシン情報のみをフィルタ
        filtered_atta_machine_informations = list(filter(lambda x: x.batting_center == related_batting_center, atta_machine_informations))
        machine_information_responses: List[MachineInformationResponseSchema] = [] # マシン情報のレスポンスを格納するリストを定義

        # マシン情報のレスポンスに必要な情報を設定し、オブジェクトをレスポンス用リストに追加
        for machine_information in filtered_atta_machine_informations:
            breaking_balls = [BreakingBallResponseSchema(id = bb.id, name = bb.name) for bb in machine_information.breaking_balls]
            ball_speeds = [BallSpeedResponseSchema(id = bs.id, speed = bs.speed) for bs in machine_information.ball_speeds]
            machine_information_responses.append(MachineInformationResponseSchema(
                id = machine_information.id,
                user_id = machine_information.user_id,
                breaking_balls = breaking_balls,
                ball_speeds = ball_speeds,
                atta_count = machine_information.count_atta(),
                nakatta_count = machine_information.count_nakatta(),
                atta = machine_information.set_atta_flag(current_user),
                nakatta = machine_information.set_nakatta_flag(current_user),
                updated = machine_information.updated
            ))
        result_list.append(BattingCenterMypageResponseSchema(
            id = related_batting_center.id,
            place_id = related_batting_center.place_id,
            name = response["name"],
            formatted_address = response["formatted_address"].split("、", 1)[-1], # "日本、"という文字列が先頭につくため加工する
            machine_informations = machine_information_responses
        ))

    return result_list
