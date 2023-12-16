import json
from typing import List, Optional

import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_cloudauth.cognito import CognitoClaims

from schema.batting_center import (
    BattingCenterGetSchema,
    BattingCenterResponseSchema,
    BattingCenterIttaUpdateSchema,
)
from schema.machine import (
    MachineInformationCreateUpdateSchema,
    MachineInformationResponseSchema,
)
from models import (
    IttaUsersCenters,
    BattingCenter,
    User,
    MachineInformation,
    AttaUserMachine,
    NakattaUserMachine,
    BreakingBall,
    BallSpeed,
)
from session import get_session
from auth import get_current_user
from env import Environment
from utils import logger


router = APIRouter()
env = Environment()

# バッティングセンター検索API
@router.post("/batting_centers/", response_model=List[BattingCenterResponseSchema])
def get_batting_centers(
    prefecture_city: str,
    current_user: CognitoClaims = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    # レスポンスで返すバッティングセンター情報を格納するリスト
    batting_centers = []

    # DBに登録済みのユーザーを取得、見つからなければ400エラー
    registered_user = session.query(User).filter(User.email == current_user.email).first()
    if registered_user is None:
        raise HTTPException(status_code=400, detail=f"{current_user.username} not exists.")

    # Google FindPlace APIへリクエスト
    payload = {"query": f"{prefecture_city} バッティングセンター","language": "ja", "key": env.find_place_api_key}
    responses = requests.get(env.find_place_url, params=payload).json()["results"]

    # FindPlace APIからのレスポンスを、prefecture_city条件に合わせてフィルタリング
    filtered_responses = list(filter(lambda x: prefecture_city in x["formatted_address"], responses))

    for response in filtered_responses:

        # レスポンスで返すバッティングセンターの情報を定義
        batting_center = BattingCenterResponseSchema(
            id = 0, # NOTE: 仮置き
            place_id = response["place_id"],
            name = response["name"],
            formatted_address = response["formatted_address"].split("、", 1)[-1], # "日本、"という文字列が先頭につくため加工する
            photos = response["photos"] if "photos" in response else None,
            itta_count = 0, # NOTE: 仮置き
            itta = "no" # NOTE: 仮置き
        )

        # API取得したバッティングセンターがDBに登録済みか確認
        registered_batting_center = session.query(BattingCenter).filter(BattingCenter.place_id == response["place_id"]).first()

        # 初めて取得したバッティングセンターはDBに登録
        if registered_batting_center is None:
            new_batting_center = BattingCenter(place_id = response["place_id"])
            session.add(new_batting_center)
            session.commit()
            session.refresh(new_batting_center)
            logger.info(f"new batting_center created id: {new_batting_center.id}, place_id: {new_batting_center.place_id}")

            # id、行った！フラグ、行った数をレスポンスに設定
            batting_center.id = new_batting_center.id
            batting_center.itta = new_batting_center.set_itta_flag(registered_user)
            batting_center.itta_count = new_batting_center.count_itta()
        else:
            batting_center.id = registered_batting_center.id
            batting_center.itta = registered_batting_center.set_itta_flag(registered_user)
            batting_center.itta_count = registered_batting_center.count_itta()

        # batting_centersリストにバッティングセンター情報を格納
        batting_centers.append(batting_center)

    return batting_centers

# バッティングセンターに行った！したユーザーの更新
@router.put("/batting_centers/{id}/itta_users", response_model=BattingCenterIttaUpdateSchema)
def update_itta_users(
    id: int,
    append_user: str,
    current_user: CognitoClaims = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    # DBに登録済みのユーザーを取得、見つからなければ400エラー
    registered_user = session.query(User).filter(User.email == current_user.email).first()
    if registered_user is None:
        raise HTTPException(status_code=400, detail=f"{current_user.username} not exists.")

    # 更新対象のバッティングセンターに行った！したユーザーを取得
    target_batting_center = session.query(BattingCenter).filter(BattingCenter.id == id).first()
    target_itta_users = target_batting_center.itta_users

    # フラグの値に応じてバッティングセンターに行った！したユーザーのリストを更新
    if append_user == "yes":
        if registered_user in target_itta_users:
            raise HTTPException(status_code=400, detail=f"{current_user.username} already registered itta! (batting_center_id: {target_batting_center.id})")
        else:
            target_itta_users.append(registered_user)
    elif append_user == "no":
        if registered_user in target_itta_users:
            target_itta_users.remove(registered_user)
        else:
            raise HTTPException(status_code=400, detail=f"{current_user.username} already deregistered itta! (batting_center_id: {target_batting_center.id})")
    else:
        raise HTTPException(status_code=400, detail="bad request")

    # 変更をDBにコミット
    target_batting_center.itta_users = target_itta_users
    session.add(target_batting_center)
    session.commit()

    return BattingCenterIttaUpdateSchema(
        id = target_batting_center.id,
        itta_count = target_batting_center.count_itta(),
        itta = target_batting_center.set_itta_flag(registered_user)
    )

# マシン情報の作成
@router.post("/batting_centers/{id}/machine_informations/")
def create_machine_information(
    id: int,
    data: MachineInformationCreateUpdateSchema,
    session: Session = Depends(get_session),
    current_user: CognitoClaims = Depends(get_current_user),
):
    # バッターボックスのリクエストが「左、右、両」以外だった場合はエラー
    if data.batter_box not in ["左", "右", "両"]:
        raise HTTPException(status_code=400, detail="bad request")

    # 投稿者と更新対象のバッティングセンターを取得
    contributor = session.query(User).filter(User.email == current_user.email).first()
    target_batting_center = session.query(BattingCenter).filter(BattingCenter.id == id).first()

    # 球種に関する情報を取得
    breaking_balls = []
    for breaking_ball_id in set(data.breaking_ball_ids):
        breaking_ball = session.query(BreakingBall).filter(BreakingBall.id == breaking_ball_id).first()
        breaking_balls.append(breaking_ball)

    # 球速に関する情報を取得
    ball_speeds = []
    for ballspeed_id in set(data.ballspeed_ids):
        ball_speed = session.query(BallSpeed).filter(BallSpeed.id == ballspeed_id).first()
        ball_speeds.append(ball_speed)

    machine_information = MachineInformation(
        user_id = contributor.id,
        batting_center_id = target_batting_center.id,
        batter_box = data.batter_box,
        breaking_balls = breaking_balls,
        ball_speeds = ball_speeds,
    )
    session.add(machine_information)
    session.commit()
    logger.info("machine information created")

    return JSONResponse(status_code=200, content={"message": "machine information created"})

# バッティングセンターごとのマシン情報の一覧取得
@router.get("/batting_centers/{id}/machine_informations/", response_model=List[MachineInformationResponseSchema])
def get_machine_informations(
    id: int,
    session: Session = Depends(get_session),
):
    machine_informations = session.query(MachineInformation).filter(MachineInformation.batting_center_id == id).all()
    return machine_informations

# マシン情報の更新
@router.put("/batting_centers/{batting_center_id}/machine_informations/{machine_information_id}")
def create_machine_information(
    batting_center_id: int,
    machine_information_id: int,
    data: MachineInformationCreateUpdateSchema,
    session: Session = Depends(get_session),
    current_user: CognitoClaims = Depends(get_current_user),
):
    # バッターボックスのリクエストが「左、右、両」以外だった場合はエラー
    if data.batter_box not in ["左", "右", "両"]:
        raise HTTPException(status_code=400, detail="bad request")

    # 更新実行ユーザーと更新対象のマシン情報を取得
    updater = session.query(User).filter(User.email == current_user.email).first()
    target_machine_information = session.query(MachineInformation).filter(MachineInformation.id == machine_information_id).first()

    # 更新者がマシン情報の投稿者でなければ、エラーを返す
    if updater != target_machine_information.user:
        raise HTTPException(status_code=400, detail="This information is created by other user.")

    # 球種に関する情報を取得
    breaking_balls = []
    for breaking_ball_id in set(data.breaking_ball_ids):
        breaking_ball = session.query(BreakingBall).filter(BreakingBall.id == breaking_ball_id).first()
        if breaking_ball is None:
            raise HTTPException(status_code=400, detail="breaking_ball is not found.")
        breaking_balls.append(breaking_ball)

    # 球速に関する情報を取得
    ball_speeds = []
    for ballspeed_id in set(data.ballspeed_ids):
        ball_speed = session.query(BallSpeed).filter(BallSpeed.id == ballspeed_id).first()
        if ball_speed is None:
            raise HTTPException(status_code=400, detail="ball_speed is not found.")
        ball_speeds.append(ball_speed)

    # 更新後のデータをコミット
    target_machine_information.batter_box = data.batter_box
    target_machine_information.breaking_balls = breaking_balls
    target_machine_information.ball_speeds = ball_speeds
    session.add(target_machine_information)
    session.commit()
    logger.info(f"machine_information updated (id: {target_machine_information.id})")

    return JSONResponse(status_code=200, content={"message": "machine information updated"})

# マシン情報の削除
@router.delete("/batting_centers/{batting_center_id}/machine_informations/{machine_information_id}")
def create_machine_information(
    batting_center_id: int,
    machine_information_id: int,
    session: Session = Depends(get_session),
    current_user: CognitoClaims = Depends(get_current_user),
):
    # 更新実行ユーザーと更新対象のマシン情報を取得
    updater = session.query(User).filter(User.email == current_user.email).first()
    target_machine_information = session.query(MachineInformation).filter(MachineInformation.id == machine_information_id).first()

    # 更新者がマシン情報の投稿者でなければ、エラーを返す
    if updater != target_machine_information.user:
        raise HTTPException(status_code=400, detail="This information is created by other user.")

    # 削除を実行
    session.delete(target_machine_information)
    session.commit()
    logger.info(f"machine_information deleted (id: {target_machine_information.id})")

    return JSONResponse(status_code=200, content={"message": "machine information deleted"})

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
