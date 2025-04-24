from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
import json
from tel_bot.models import OrderModel


load_dotenv()
app = FastAPI()
MY_TOKEN = os.getenv('MY_TOKEN')
USER_ID = os.getenv('USER_ID')
ORGANIZATION_ID = os.getenv('ORGANIZATION_ID')
headers = {'Authorization': f'Bearer {MY_TOKEN}', 'Content-Type': 'application/json'}
params = [
    ("filter", "updated>=2019-07-10 12:00:00;updated<=2019-07-12 12:00:00")
]

urls = {
    'href_user': f"https://api.moysklad.ru/api/remap/1.2/entity/counterparty/{USER_ID}",
    'href_organization': f"https://api.moysklad.ru/api/remap/1.2/entity/organization/{ORGANIZATION_ID}",
    'get_product': 'https://api.moysklad.ru/api/remap/1.2/entity/product',
    'get_employee': 'https://api.moysklad.ru/api/remap/1.2/context/employee',
    'customerorder': 'https://api.moysklad.ru/api/remap/1.2/entity/customerorder',
    'productfolder': 'https://api.moysklad.ru/api/remap/1.2/entity/productfolder',
    'get_assortment': 'https://api.moysklad.ru/api/remap/1.2/entity/assortment?filter=productFolder=https://api.moysklad.ru/api/remap/1.2/entity/productfolder/',
}


@app.get('/all_products')
def get_all_product():
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
    if response.status_code == 200:
        return filter_prodicts
    return {'status_code': response.status_code}


@app.get('/productfolder')
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
    return {'status_code': response.status_code}



def get_filter_products(json_response):
    result = {}
    result['meta'] = {
        'size': json_response.get('meta').get('size'),
        'limit': json_response.get('meta').get('limit'),
        'offset': json_response.get('meta').get('offset'),
    }

    producs = []
    for data_product in json_response.get('rows'):
        product = {}
        product['id'] = data_product.get('id')
        product['name'] = data_product.get('name')
        product['description'] = data_product.get('description')
        product['code'] = data_product.get('code')
        product['pathName'] = data_product.get('pathName')
        product['salePrices'] = data_product.get('salePrices')[0].get('value')
        product['images'] = [prod.get('miniature', {}).get('downloadHref', '') for prod in product.get('images', {}).get('rows', {})]
        producs.append(product)
    result['products'] = producs
    return result


@app.get('/product')
def get_product(id_group=None, search=None, limit=5, offset=0):
    params = {
        'search': search,
        'limit': limit,
        'offset': offset,
        'expand': 'images'
    }
    if search:
        response = requests.get(url=urls['get_product'], params=params, headers=headers)
        if response.status_code == 200:
            get_products = response.json()
            return get_filter_products(get_products)
        return {'status_code': response.status_code}
    if id_group:
        response = requests.get(url=urls['get_assortment'], params=params, headers=headers)
        if response.status_code == 200:
            get_products = response.json()
            return get_filter_products(get_products)
        return {'status_code': response.status_code}
    response = requests.get(url=urls['get_product'], params=params, headers=headers)
    if response.status_code == 200:
        get_products = response.json()
        return get_filter_products(get_products)
    return {'status_code': response.status_code}


@app.post('/product_order')
def customerorder(data: OrderModel):
    VALUE_DATA = {
        'organization': {
            "meta": {
                "href": urls['href_organization'],
                "type": "organization",
                "mediaType": "application/json"
              }
        },
        "agent": {
            "meta": {
                "href": urls['href_user'],
                "type": "counterparty",
                "mediaType": "application/json"
              }
            },
        "positions": [],
    }
    headers = {'Authorization': f'Bearer {MY_TOKEN}', 'Accept-Encoding': 'gzip', 'Content-Type': 'application/json'}
    for item in data.items:
        VALUE_DATA['positions'].append({
                            "quantity": item.counter,
                            "assortment": {
                                "meta": {
                                    "href": f'{urls.get("get_product")}/' + item.id_prod,
                                    "type": "product",
                                    "mediaType": "application/json"
                                    }
                                }
                            })

    response = requests.post(url=urls['customerorder'], headers=headers, data=json.dumps(VALUE_DATA))
    if response.status_code == 200:
        return response.json()
    return {'status_code': response.status_code}

