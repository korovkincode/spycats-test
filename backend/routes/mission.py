from fastapi import APIRouter, HTTPException, Depends
from models.mission import MissionModel
import uuid
from typing import Annotated
from sqlalchemy.orm import Session
from config.database import Database
from config.models import Missions, Targets


router = APIRouter()
driverDep = Annotated[Session, Depends(lambda: Database.getDriver())]


@router.post("/", response_model=None)
async def create(missionData: MissionModel, driver: driverDep) -> HTTPException | dict:
    missionData = missionData.model_dump()

    missionData["ID"] = uuid.uuid4().hex
    mission = Missions(
        ID=missionData["ID"], cat=missionData["catID"], complete=False
    )
    driver.add(mission)
    driver.commit()

    targetIndex = 0
    for targetData in missionData["targets"]:
        missionData["targets"][targetIndex]["ID"] = uuid.uuid4().hex

        target = Targets(
            ID=missionData["targets"][targetIndex]["ID"], mission=missionData["ID"],
            name=targetData["name"], country=targetData["country"],
            notes=targetData["notes"], complete=False
        )
        driver.add(target)
        driver.commit()

        targetIndex += 1

    return {
        "message": "Successfully added",
        "data": missionData
    }    


@router.get("/{missionID}", response_model=None)
async def read(missionID: str, driver: driverDep) -> HTTPException | dict:
    if missionID == "all":
        missionData = driver.query(Missions).all()
    else:
        missionData = driver.query(Missions).filter(Missions.ID == missionID).first()

    if not missionData:
        raise HTTPException(
            status_code=404, detail="No such mission"
        )

    return {
        "message": "Successfull retrieving",
        "data": missionData
    }


@router.delete("/{missionID}", response_model=None)
async def delete(missionID: str, driver: driverDep) -> HTTPException | dict:
    findMission = driver.query(Missions).filter(Missions.ID == missionID).first()
    if not findMission:
        raise HTTPException(
            status_code=404, detail="No such missions"
        )
    if findMission.cat:
        raise HTTPException(
            status_code=404, detail=f"Cat #{findMission.cat} is already assigned to this mission"
        )
    
    driver.query(Missions).filter(Missions.ID == missionID).delete()
    driver.commit()

    return {
        "message": "Successfully deleted"
    }