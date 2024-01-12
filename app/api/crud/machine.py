from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import MachineInformation

def get_machine_information_by_id(session: Session, id: int):
    machine_information = session.query(MachineInformation).filter(MachineInformation.id == id).first()
    if machine_information is None:
        raise HTTPException(status_code=400, detail=f"machine_information with id:{id} not exists.")

    return machine_information

def get_machine_informations_by_batting_center_id(session: Session, batting_center_id: int):
    machine_informations = session.query(MachineInformation).filter(MachineInformation.batting_center_id == batting_center_id).all()
    if machine_informations is None:
        raise HTTPException(status_code=400, detail=f"machine_informations with batting_center_id:{batting_center_id} not exists.")

    return machine_informations
