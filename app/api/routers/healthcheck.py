from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from session import get_session

router = APIRouter()

@router.get("/healthcheck")
def healthcheck(
    session: Session = Depends(get_session)
):
    row = session.execute(text("SELECT 'OK' as status")).first()
    return {"status": row.status}
