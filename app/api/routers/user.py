from typing import List, Optional

import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_cloudauth.cognito import CognitoClaims

from models import User, BattingCenter, MachineInformation
from session import get_session
from schema.user import (
    UserLoginSchema,
    UserResponseSchema,
    UpdateIttaSchema,
    UpdateAttaNakattaSchema,
)
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
