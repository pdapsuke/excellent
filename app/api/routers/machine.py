import json
from typing import List

import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends, HTTPException
from schema.batting_center import (
    BattingCenterGetSchema,
    BattingCenterResponseSchema,
)

from schema.machine import (
    MachineInformationCreateSchema,
    MachineInformationResponseSchema,
    MachineInformationConfigSchema
)


from models import IttaUsersCenters, BattingCenter, User, MachineInformation
from session import get_session

router = APIRouter()

@router.get("/machine_informations/{place_id}", response_model=List[MachineInformationResponseSchema])
def get_machine_information(
    place_id: str,
    session: Session = Depends(get_session),
):
    machine_informations = session.query(MachineInformation).filter(BattingCenter.place_id == place_id).all()
    for machine_information in machine_informations:
        machine_information.config = json.loads(machine_information.config)

    return machine_informations


@router.post("/machine_informations/", response_model=MachineInformationResponseSchema)
def create_machine_information(
    data: MachineInformationCreateSchema,
    session: Session = Depends(get_session),
):
    current_user = session.query(User).filter(User.username == data.username).first()
    target_batting_center = session.query(BattingCenter).filter(BattingCenter.place_id == data.place_id).first()
    config = {
        "ballspeed": data.ballspeed,
        "pitch_type": data.pitch_type,
        "batter_box": data.batter_box,
        }
    
    machine_information = MachineInformation(
        config = json.dumps(config, ensure_ascii=False),
        user = current_user,
        batting_center = target_batting_center
    )
    session.add(machine_information)
    session.commit()
    session.refresh(machine_information)

    machine_information.config = config

    return machine_information