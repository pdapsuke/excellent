from typing import Optional, List
from pydantic import BaseModel

class BattingCenterGetSchema(BaseModel):
    prefecture_city: str
