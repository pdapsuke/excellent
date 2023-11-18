from typing import Optional, List
from pydantic import BaseModel

from schema.machine import MachineInformationResponseSchema

class BattingCenterGetSchema(BaseModel):
    prefecture_city: str
    username: str

class BattingCenterResponseSchema(BaseModel):
    id: int
    name: str
    place_id: str
    machine_informations: List[MachineInformationResponseSchema]
