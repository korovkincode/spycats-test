from pydantic import BaseModel
from pydantic import model_validator
import json


class AbstractModel(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def validateToJSON(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value