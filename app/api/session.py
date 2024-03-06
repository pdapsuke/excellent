from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import Utils
from env import Environment

def get_db_url():
    secret = Utils.get_db_secret(Utils.get_ttl_hash())
    return f"mysql+pymysql://{secret.db_user}:{secret.db_password}@{secret.db_host}:{secret.db_port}/{env.db_name}?charset=utf8mb4"

env = Environment()
SQLALCHEMY_DATABASE_URL = get_db_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = True, bind=engine)

def get_session():
    """DBのセッションを生成する。
    1リクエスト1セッションの想定で、 レスポンスが返却される際に自動でcloseされる。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()