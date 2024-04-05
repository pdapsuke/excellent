import enum

from pydantic_settings import BaseSettings

class Mode(str, enum.Enum):
    PRD = "prd"
    STG = "stg"
    DEV = "dev"
    LOCAL = "local"

class Environment(BaseSettings):
    db_name: str
    aws_region: str
    cognito_userpool_id: str
    cognito_client_id: str
    find_place_url: str
    place_details_url: str
    find_place_api_key: str
    photo_reference_url: str
    mode: Mode
    db_secret_name: str
    resas_api_prefecture_url: str
    resas_api_city_url: str
    resas_api_key: str