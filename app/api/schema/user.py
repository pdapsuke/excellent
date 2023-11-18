from typing import Optional, List

from pydantic import BaseModel

from schema.batting_center import BattingCenterResponseSchema
from schema.machine import MachineInformationResponseSchema

class UserLoginSchema(BaseModel):
    jwt_token: str

class UserResponseSchema(BaseModel):
    username: str
    email: str
    itta_centers: List[BattingCenterResponseSchema]
    machine_informations: List[MachineInformationResponseSchema]

    class Config:
        orm_mode = True
    
class UpdateIttaSchema(BaseModel):
    username: str
    place_id: str
    itta: str
