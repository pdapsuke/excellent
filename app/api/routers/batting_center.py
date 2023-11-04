import requests
from fastapi import APIRouter, Response
from schema.batting_center import (
    BattingCenterGetSchema,
)

router = APIRouter()

# Find Place
@router.post("/batting_centers/")
def get_batting_centers(
    data: BattingCenterGetSchema
):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    payload = {"query": f"{data.prefecture_city} バッティングセンター","language": "ja", "key": "***REMOVED***"}
    response = requests.get(url, params=payload)
    return response.json()["results"]
