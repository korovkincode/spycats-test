from models.abstract import AbstractModel


class TargetModel(AbstractModel):
    name: str
    country: str
    notes: str