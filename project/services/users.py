from utils.repositories import AbstractRepository
from classes.error import ServiceError

import jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta


SECRET_KEY = 'someadkandfaemfamfmsecretaposdadmamdamkammafkeyasdladalmdsdaamiraisdmasm'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE = 10800

pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_token(data: dict, expires: timedelta):
    to_encode = data.copy()

    if expires:
        expire = datetime.now() + expires
    else:
        expire = datetime.now() + timedelta(minutes = 120)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt
    

class UsersService:

    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def create_user(self, login: str, password: str):
        try:

            hash_password = get_password_hash(password)

            data = {
                'login': login,
                'password': hash_password
            } 

            result  = await self.users_repo.add(data = data)
            return result
        except Exception as error:
            raise ServiceError(
                message = f"Service Error: Add New: {str(error)}",
                status_code = 400
            )
        
    async def get_user(self, filters: dict):
        try:
            result = await self.users_repo.select(filters = filters)
            return result
        except Exception as error:
            raise ServiceError(
                message = f"Service Error: Get: {str(error)}",
                status_code = 400
            )
        
    async def user_sign_in(self, login: str, password: str):
        filters = {
            'login': login
        }

        try:
            find_user = await self.users_repo.select(filters = filters)

            if not find_user:
                return {
                    'message': 'User Not Found',
                    'status_code': 404
                }
            
            if not verify_password(password, find_user[0].password):
                return {
                    'message': "Wrong User's Password",
                    'status_code': 401
                }

            data = {
                'user_id': find_user[0].id,
                'user_level': find_user[0].level
            }

            token = create_token(data, expires = timedelta(minutes = 180))

            return {
                'message': 'Success',
                'data': {
                    'token': token,
                    'token_type': "Bearer"
                }
            }

        except Exception as error:
            raise ServiceError(
                message = f"Service Error: Sign In: {str(error)}",
                status_code = 400
            )

    async def check_token(self, token: str):
        try:
            to_decode = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

            user_id = to_decode.get("user_id")

            if not user_id:
                raise ServiceError(
                    message = "user id in token not found: Invalid Token",
                    status_code = 401
                )
            
            find_user = await self.users_repo.select(filters = {'id': user_id})

            if not find_user:
                return {
                    'message': 'User Not Found',
                    'status_code': 404
                }
            
            return {
                'message': 'Valid Token',
                'status_code': 200
            }
        except jwt.InvalidTokenError:
            return {
                'message': f'Service Response: Invalid Token',
                'status_code': 401
            }
        except Exception as error:
            raise ServiceError(
                message = f"Service Error: Check token: {str(error)}",
                status_code = 400
            )

