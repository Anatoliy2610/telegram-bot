from tel_bot.database import SessionLocal
from fastapi import HTTPException


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_status_code(status_code, message, result):
    if status_code == 200:
        return result
    return HTTPException(status_code=404, detail=message)


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
