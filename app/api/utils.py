from functools import lru_cache
import json
from logging import getLogger
import time
from typing import Dict

import boto3
from pydantic import BaseModel

from env import Environment, Mode

env = Environment()

# ロガーの設定
logger = getLogger("uvicorn.app")

class RdsSecret(BaseModel):
    db_user: str
    db_password: str
    db_host: str
    db_port: int

class Utils:
    @staticmethod
    def get_ttl_hash(seconds: int = 600) -> int:
        return round(time.time() / seconds)

    @staticmethod
    def get_secret(secret_name: str, aws_region: str) -> Dict[str, str]:
        session = boto3.session.Session()
        client = session.client(
            service_name = 'secretsmanager',
            region_name = aws_region
        )
        get_secret_value_response = client.get_secret_value(
            SecretId = secret_name
        )
        return json.loads(get_secret_value_response['SecretString'])

    @staticmethod
    @lru_cache
    def get_db_secret(get_ttl_hash: int = -1, env: Environment = env) -> RdsSecret:
        if (env.mode == Mode.LOCAL):
            secret = {
                "db_user": "root",
                "db_password": "root1234",
                "db_host": "127.0.0.1",
                "db_port": "63306",
            }
        else:
            secret = Utils.get_secret(env.db_secret_name, env.aws_region)
        return RdsSecret.parse_obj(secret)
