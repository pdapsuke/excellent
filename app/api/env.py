from pydantic_settings import BaseSettings

class Environment(BaseSettings):
    db_user: str
    db_password: str
    db_port: str
    db_host: str
    db_name: str
    aws_region: str
    cognito_userpool_id: str
    cognito_client_id: str
    find_place_url: str
    place_details_url: str
    find_place_api_key: str
    photo_reference_url: str
