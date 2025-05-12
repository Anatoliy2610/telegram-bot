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
from tel_bot.carts.shemas import CartAdd
from tel_bot.config import headers


router = APIRouter(tags=['Корзина'])


@router.get("/cart", response_model=List[Cart])
async def get_cart(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    response = db.query(CartModel).filter(CartModel.user_id == user_data.id).all()
    for product in response:
        new_response = requests.get(url=f"{urls['get_product']}/{product.product_id}", headers=headers).json()
    return response


@router.post("/cart/add")
async def add_to_cart(product_data: CartAdd, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    check_product_id = db.query(CartModel).filter(CartModel.product_id == product_data.id, CartModel.user_id == user_data.id).first()
    if check_product_id:
        check_product_id.product_count = product_data.count
        response = requests.get(url=f"{urls['get_product']}/{product_data.id}", headers=headers).json()
        check_product_id.product_name = response['name']
        db.commit()
        db.refresh(check_product_id)
        return {'Изменено': {
            'user_id': user_data.id,
            'product_id': product_data.id,
            'product_count': product_data.count,
        }}
    db_product = CartModel(
        user_id=user_data.id,
        product_id=product_data.id,
        product_count = product_data.count,
        product_name = requests.get(url=f"{urls['get_product']}/{product_data.id}", headers=headers).json()['name']
        )
    db_product.product_name
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {'Добавлено': {
        'user_id': user_data.id,
        'product_id': product_data.id,
        'product_count': product_data.count,
    }}
