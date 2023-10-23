from pydantic_settings import BaseSettings

class Environment(BaseSettings):
    db_user: str
    db_password: str
    db_port: str
    db_host: str
    db_name: str
