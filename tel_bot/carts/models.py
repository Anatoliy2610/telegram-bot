from pydantic import BaseModel
from typing import Optional
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship


from tel_bot.database import Base


class Cart(BaseModel):
    user_id: int
    product_id: str
    product_count: int
    product_name: str


class CartModel(Base):
    __tablename__ = 'carts'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    product_id = Column(String, primary_key=True)
    product_count = Column(Integer)
    product_name = Column(String)
       
    product = relationship("UserModel")

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'product_id'),
       )
