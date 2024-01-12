from typing import List

from fastapi import HTTPException
import requests
from sqlalchemy.orm import Session

from env import Environment
from models import MachineInformation, User
from schema.batting_center import BattingCenterMypageResponseSchema
from schema.machine import (
    MachineInformationResponseSchema,
    BreakingBallResponseSchema,
    BallSpeedResponseSchema,
)

env = Environment()

# DBに登録済みのユーザーを取得、見つからなければ400エラー
def get_user_by_email(session: Session, email: str):
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=400, detail=f"user whose email is {email} not exists.")

    return user

# マイページ（投稿、あった！、なかった！したマシン情報と紐づくバッティングセンター）を表示するレスポンスを生成する処理
def create_mypage_response(current_user: User, target_machine_informations: List[MachineInformation]) -> List[BattingCenterMypageResponseSchema]:

    # 処理の結果を格納するリスト
    result_list: List[BattingCenterMypageResponseSchema] = []

    # 対象マシン情報に関連するバッティングセンターを取得
    related_batting_centers = set([mi.batting_center for mi in target_machine_informations])

    # 関連するバッティングセンターごとにマイページレスポンス用オブジェクトを作成し、レスポンス格納リストに追加していく
    for related_batting_center in related_batting_centers:

        # Google PlaceDetails APIへ施設名と住所をリクエスト
        payload = {"place_id": related_batting_center.place_id, "language": "ja", "fields": "name,formatted_address", "key": env.find_place_api_key}
        response = requests.get(env.place_details_url, params=payload).json()["result"]

        # バッティングセンターに関連するマシン情報のみをフィルタ
        filtered_posted_machine_informations = list(filter(lambda x: x.batting_center == related_batting_center, target_machine_informations))
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
