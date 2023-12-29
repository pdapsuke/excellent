from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import User

# DBに登録済みのユーザーを取得、見つからなければ400エラー
def get_user_by_email(session: Session, email: str):
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=400, detail=f"user whose email is {email} not exists.")

    return user
