from fastapi import APIRouter
import requests

from env import Environment

router = APIRouter()
env = Environment()

# 都道府県一覧を取得する
@router.get("/prefecture/")
def get_prefecture():
    headers = {"X-API-KEY": f"{env.resas_api_key}"}
    response = requests.get(f"{env.resas_api_prefecture_url}", headers=headers).json()
    return response["result"]

# 市区町村一覧を取得する
@router.get("/city/{prefCode}")
def get_city(prefCode: int):
    headers = {"X-API-KEY": f"{env.resas_api_key}"}
    payload = {"prefCode": prefCode}
    response = requests.get(f"{env.resas_api_city_url}", headers=headers, params=payload).json()
    return response["result"]
