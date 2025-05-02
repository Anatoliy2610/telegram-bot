from pydantic import BaseModel
from typing import List


class OrderModelBase(BaseModel):
    id_prod: str
    counter: int


class OrderModel(BaseModel):
    items: List[OrderModelBase]
