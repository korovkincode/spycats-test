from models.abstract import AbstractModel
from typing import List
from models.target import TargetModel


class MissionModel(AbstractModel):
    catID: str
    targets: List[TargetModel]