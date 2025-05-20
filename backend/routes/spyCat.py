from fastapi import APIRouter, HTTPException, Depends
from models.spyCat import SpyCatModel
import utils
import uuid
from typing import Annotated
from sqlalchemy.orm import Session
from config.database import Database
from config.models import SpyCats


router = APIRouter()
driverDep = Annotated[Session, Depends(lambda: Database.getDriver())]


@router.post("/", response_model=None)
async def create(spyCatData: SpyCatModel, driver: driverDep) -> HTTPException | dict:
    spyCatData = spyCatData.model_dump()
    if not utils.validateBreed(spyCatData["breed"]):
        raise HTTPException(
            status_code=403, detail="Breed cannot be validated"
        )

    spyCatData["ID"] = uuid.uuid4().hex
    spyCat = SpyCats(
        ID=spyCatData["ID"], name=spyCatData["name"], experience=spyCatData["experience"],
        breed=spyCatData["breed"], salary=spyCatData["salary"]
    )
    driver.add(spyCat)
    driver.commit()

    return {
        "message": "Successfully added",
        "data": spyCatData
    }


@router.get("/{catID}", response_model=None)
async def read(catID: str, driver: driverDep) -> HTTPException | dict:
    if catID == "all":
        spyCatData = driver.query(SpyCats).all()
    else:
        spyCatData = driver.query(SpyCats).filter(SpyCats.ID == catID).first()
        
    if not spyCatData:
        raise HTTPException(
            status_code=404, detail="No such spy cat"
        )

    return {
        "message": "Successfull retrieving",
        "data": spyCatData
    }


@router.put("/{catID}", response_model=None)
async def update(catID: str, newSalary: int, driver: driverDep) -> HTTPException | dict:
    if not driver.query(SpyCats).filter(SpyCats.ID == catID).first():
        raise HTTPException(
            status_code=404, detail="No such spy cat"
        )

    driver.query(SpyCats).filter(SpyCats.ID == catID).update({
        SpyCats.salary: newSalary
    })
    driver.commit()

    return {
        "message": "Successfully updated"
    }


@router.delete("/{catID}", response_model=None)
async def delete(catID: str, driver: driverDep) -> HTTPException | dict:
    if not driver.query(SpyCats).filter(SpyCats.ID == catID).first():
        raise HTTPException(
            status_code=404, detail="No such spy cat"
        )
    
    driver.query(SpyCats).filter(SpyCats.ID == catID).delete()
    driver.commit()

    return {
        "message": "Successfully deleted"
    }