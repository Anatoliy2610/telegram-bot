from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer


load_dotenv()
MY_TOKEN_MS = os.getenv('MY_TOKEN_MS')
USER_ID = os.getenv('USER_ID')
ORGANIZATION_ID = os.getenv('ORGANIZATION_ID')
headers = {'Authorization': f'Bearer {MY_TOKEN_MS}', 'Content-Type': 'application/json'}
SECRET_KEY_TOKEN = os.getenv('SECRET_KEY_TOKEN')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

urls = {
    'href_user': f"https://api.moysklad.ru/api/remap/1.2/entity/counterparty/{USER_ID}",
    'href_organization': f"https://api.moysklad.ru/api/remap/1.2/entity/organization/{ORGANIZATION_ID}",
    'get_product': 'https://api.moysklad.ru/api/remap/1.2/entity/product',
    'get_employee': 'https://api.moysklad.ru/api/remap/1.2/context/employee',
    'customerorder': 'https://api.moysklad.ru/api/remap/1.2/entity/customerorder',
    'productfolder': 'https://api.moysklad.ru/api/remap/1.2/entity/productfolder',
    'get_assortment': 'https://api.moysklad.ru/api/remap/1.2/entity/assortment?filter=productFolder=https://api.moysklad.ru/api/remap/1.2/entity/productfolder/',
}

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
