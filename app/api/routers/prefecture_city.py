from fastapi import APIRouter
import requests

router = APIRouter()

# 都道府県一覧を取得する
@router.get("/prefecture/")
def get_prefecture():
    url = "https://opendata.resas-portal.go.jp/api/v1/prefectures"
    api_key = "***REMOVED***"
    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers).json()
    return response["result"]

# 市区町村一覧を取得する
@router.get("/city/{prefCode}")
def get_city(prefCode: int):
    url = "https://opendata.resas-portal.go.jp/api/v1/cities"
    api_key = "***REMOVED***"
    headers = {"X-API-KEY": api_key}
    payload = {"prefCode": prefCode}
    response = requests.get(url, headers=headers, params=payload).json()
    return response["result"]

