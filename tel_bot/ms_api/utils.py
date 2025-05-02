from fastapi import HTTPException


def get_data_or_exception(status_code, message, data):
    if status_code != 200:
        HTTPException(status_code, detail=message)
    return data


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
