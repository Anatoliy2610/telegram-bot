from fastapi import APIRouter, Depends, HTTPException, status
import requests
import json
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List


from tel_bot.contants import urls, headers, VALUE_DATA
from tel_bot.utils import get_db, get_status_code, get_filter_products
from tel_bot.models import OrderModel, User, UserCreate, UserInDB, UserModel, CartModel, Cart
from tel_bot.users.pass_conf import hash_password, verify_password
from tel_bot.users.token_jwt import create_access_token, get_current_user

router = APIRouter()


@router.get('/all_products')
def all_products():
    response = requests.get(url=urls['get_product'], headers=headers)
    get_products = response.json()
    filter_prodicts = []
    for product in get_products['rows']:
        products = {}
        products['id'] = product.get('id')
        products['name'] = product.get('name')
        products['description'] = product.get('description')
        products['code'] = product.get('code')
        products['pathName'] = product.get('pathName')
        products['salePrices'] = product.get('salePrices')[0].get('value')
        products['images'] = product.get('images').get('meta').get('href')
        filter_prodicts.append(products)
    return get_status_code(status_code=response.status_code, result=filter_prodicts, message='Страница не найдена')


@router.get('/productfolder')
def get_productfolder():
    response = requests.get(url=(urls['productfolder']), headers=headers)
    if response.status_code == 200:
        group_products = response.json()
        result = []
        for group in group_products['rows']:
            group_data = {}
            group_data['href'] = group.get('meta').get('href')
            group_data['id'] = group.get('id')
            group_data['name'] = group.get('name')
            group_data['description'] = group.get('description')
            result.append(group_data)
        return result
    return HTTPException(status_code=404, detail='Страница не найдена')



@router.get('/product')
def get_product(id_group=None, search=None, limit=5, offset=0):
    params = {
        'search': search,
        'limit': limit,
        'offset': offset,
        'expand': 'images'
    }
    if search:
        response = requests.get(url=urls['get_product'], params=params, headers=headers)
        return get_status_code(
            status_code=response.status_code,
            result=get_filter_products(response.json()),
            message='Страница не найдена')
    if id_group:
        response = requests.get(url=urls['get_assortment'], params=params, headers=headers)
        return get_status_code(
            status_code=response.status_code,
            result=get_filter_products(response.json()),
            message='Страница не найдена')
    response = requests.get(url=urls['get_product'], params=params, headers=headers)
    return get_status_code(
        status_code=response.status_code,
        result=get_filter_products(response.json()),
        message='Страница не найдена')


@router.post('/product_order')
def customerorder(data: OrderModel):
    for item in data.items:
        VALUE_DATA['positions'].append(
            {
                "quantity": item.counter,
                "assortment": {
                    "meta": {
                        "href": f'{urls.get("get_product")}/' + item.id_prod,
                        "type": "product",
                        "mediaType": "application/json"
                        }
                    }
            }
        )
    response = requests.post(url=urls['customerorder'], headers=headers, data=json.dumps(VALUE_DATA))
    return get_status_code(
        status_code=response.status_code,
        result=response.json(),
        message='Страница не найдена')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким названием существует")
    db_user = UserModel(
        username=user.username,
        email=user.email,
        full_name = user.full_name,
        hash_password = hash_password(user.password)
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user


@router.get("/users", response_model=List[User])
async def register(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hash_password):
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/cart/add")
async def add_to_cart(user_id: int, product_id: str, product_count: int, db: Session = Depends(get_db)):
    db_product = CartModel(
        user_id=user_id,
        product_id=product_id,
        product_count = product_count,
        )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {'Добавлено': {
        'user_id': user_id,
        'product_id': product_id,
        'product_count': product_count,
    }}


@router.get("/cart", response_model=List[Cart])
async def get_cart(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(CartModel).filter(CartModel.user_id == current_user.id).all()
