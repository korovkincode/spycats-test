from fastapi import APIRouter, HTTPException, Depends
from models.target import TargetModel
from typing import Annotated
from sqlalchemy.orm import Session
from config.database import Database
from config.models import Targets
from typing import Optional


router = APIRouter()
driverDep = Annotated[Session, Depends(lambda: Database.getDriver())]


@router.get("/{targetID}", response_model=None)
async def read(targetID: str, driver: driverDep) -> HTTPException | dict:
    if targetID == "all":
        targetData = driver.query(Targets).all()
    else:
        targetData = driver.query(Targets).filter(Targets.ID == targetID).first()

    if not targetData:
        raise HTTPException(
            status_code=404, detail="No such target"
        )

    return {
        "message": "Successfull retrieving",
        "data": targetData
    }


@router.get("/of/{missionID}", response_model=None)
async def readMission(missionID: str, driver: driverDep) -> HTTPException | dict:
    targetMissionData = driver.query(Targets).filter(Targets.mission == missionID).all()

    return {
        "message": "Successfull retrieving",
        "data": targetMissionData
    }


@router.put("/{targetID}", response_model=None)
async def update(targetID: str, driver: driverDep, notes: Optional[str] = None, complete: Optional[bool] = None) -> HTTPException | dict:
    if not driver.query(Targets).filter(Targets.ID == targetID).first():
        raise HTTPException(
            status_code=404, detail="No such target"
        )

    newTarget = {}
    if notes:
        newTarget[Targets.notes] = notes
    if complete:
        newTarget[Targets.complete] = complete

    driver.query(Targets).filter(Targets.ID == targetID).update(newTarget)
    driver.commit()

    return {
        "message": "Successfully updated"
    }