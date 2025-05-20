from models.abstract import AbstractModel
from typing import Optional


class SpyCatModel(AbstractModel):
    name: str
    experience: int
    breed: str
    salary: int