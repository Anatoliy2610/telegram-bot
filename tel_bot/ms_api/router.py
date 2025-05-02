from fastapi import APIRouter, HTTPException, Depends
import requests
import json
from copy import deepcopy
from sqlalchemy.orm import Session

from tel_bot.config import urls, headers, VALUE_DATA
from tel_bot.ms_api.utils import get_data_or_exception, get_filter_products
from tel_bot.ms_api.models import OrderModel
from tel_bot.users.utils import get_current_user
from tel_bot.users.models import UserModel
from tel_bot.carts.models import CartModel
from tel_bot.users.utils import get_db


router = APIRouter(tags=['Мой склад'])


@router.get('/all_products')
def all_products(user_data: UserModel = Depends(get_current_user)):
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
    return get_data_or_exception(
        status_code=response.status_code,
        data=filter_prodicts,
        message=f'Статус код - {response.status_code}')


@router.get('/productfolder')
def get_productfolder(user_data: UserModel = Depends(get_current_user)):
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
    return HTTPException(
        status_code=404,
        detail=f'Статус код - {response.status_code}'
        )


@router.get('/product')
def get_product(id_group=None, search=None, limit=5, offset=0, user_data: UserModel = Depends(get_current_user)):
    params = {
        'search': search,
        'limit': limit,
        'offset': offset,
        'expand': 'images'
    }
    if search:
        response = requests.get(url=urls['get_product'], params=params, headers=headers)
        return get_data_or_exception(
            status_code=response.status_code,
            data=get_filter_products(response.json()),
            message=f'Статус код - {response.status_code}')
    if id_group:
        response = requests.get(url=urls['get_assortment'], params=params, headers=headers)
        return get_data_or_exception(
            status_code=response.status_code,
            data=get_filter_products(response.json()),
            message=f'Статус код - {response.status_code}')
    response = requests.get(url=urls['get_product'], params=params, headers=headers)
    return get_data_or_exception(
        status_code=response.status_code,
        data=get_filter_products(response.json()),
        message=f'Статус код - {response.status_code}')


# @router.post('/product_order')
# def customerorder(data: OrderModel, user_data: UserModel = Depends(get_current_user)):
#     '''
#     заказ без корзины
#     '''
#     for item in data.items:
#         VALUE_DATA['positions'].append(
#             {
#                 "quantity": item.counter,
#                 "assortment": {
#                     "meta": {
#                         "href": f'{urls.get("get_product")}/' + item.id_prod,
#                         "type": "product",
#                         "mediaType": "application/json"
#                         }
#                     }
#             }
#         )
#     response = requests.post(url=urls['customerorder'], headers=headers, data=json.dumps(VALUE_DATA))
#     return get_data_or_exception(
#         status_code=response.status_code,
#         result=response.json(),
#         message=f'Статус код - {response.status_code}')


@router.post('/product_order')
def customerorder(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    заказ из корзины
    '''
    data = db.query(CartModel).filter(CartModel.user_id == user_data.id).all()
    value_data = deepcopy(VALUE_DATA)
    for product in data:
        value_data['positions'].append(
            {
                "quantity": product.product_count,
                "assortment": {
                    "meta": {
                        "href": f'{urls.get("get_product")}/' + product.product_id,
                        "type": "product",
                        "mediaType": "application/json"
                        }
                    }
            }
        )
    return value_data
    # response = requests.post(url=urls['customerorder'], headers=headers, data=json.dumps(VALUE_DATA))
    # return get_data_or_exception(
    #     status_code=response.status_code,
    #     result=response.json(),
    #     message=f'Статус код - {response.status_code}')
