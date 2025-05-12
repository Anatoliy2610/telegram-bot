from pydantic import BaseModel


class CartAdd(BaseModel):
    id: str
    count: int
