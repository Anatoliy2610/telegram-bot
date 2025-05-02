from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import requests
import json
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List


from tel_bot.config import urls, headers, VALUE_DATA
from tel_bot.users.utils import get_db
from tel_bot.carts.models import CartModel, Cart
from tel_bot.users.utils import get_current_user
from tel_bot.users.models import UserModel


router = APIRouter(tags=['Корзина'])


@router.get("/cart", response_model=List[Cart])
async def get_cart(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(CartModel).filter(CartModel.user_id == user_data.id).all()


@router.post("/cart/add")
async def add_to_cart(product_id: str, product_count: int, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    check_product_id = db.query(CartModel).filter(CartModel.product_id == product_id, CartModel.user_id == user_data.id).first()
    if check_product_id:
        check_product_id.product_count = product_count
        db.commit()
        db.refresh(check_product_id)
        return {'Изменено': {
            'user_id': user_data.id,
            'product_id': product_id,
            'product_count': product_count,
        }}
    db_product = CartModel(
        user_id=user_data.id,
        product_id=product_id,
        product_count = product_count,
        )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {'Добавлено': {
        'user_id': user_data.id,
        'product_id': product_id,
        'product_count': product_count,
    }}
