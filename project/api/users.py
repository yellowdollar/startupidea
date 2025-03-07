from fastapi import APIRouter
from fastapi import Depends, Form, HTTPException, status

from typing import Annotated, Optional

from services.users import UsersService
from api.dependencies import users_service


user_router = APIRouter(
    prefix = "/users"
)

@user_router.post('/create_new_user')
async def create_new_user(
    users_service: Annotated[UsersService, Depends(users_service)],
    login: str = Form(...),
    password: str = Form(...)
):
    try:
        result = await users_service.create_user(login = login, password = password)
        return result
    except Exception as error:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"API Error: {str(error)}"
        )
    
@user_router.post('/sign_in')
async def sign_in(
    users_service: Annotated[UsersService, Depends(users_service)],
    login: str = Form(...),
    password: str = Form(...)
):
    try:
        result = await users_service.user_sign_in(login = login, password = password)
        return result
    except Exception as error:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"API Error: {str(error)}"
        )

@user_router.get('/')
async def get_user(
    users_service: Annotated[UsersService, Depends(users_service)],
    token: str = None,
    id: Optional[int] = None
):
    
    user_check = await users_service.check_token(token)

    if user_check['status_code'] != 200:
        return {
            'message': 'API Response: Invalid Token',
            'status_code': status.HTTP_401_UNAUTHORIZED
        }

    filters = {}
    
    if id is not None:
        filters['id'] = id
    
    try:
        result =  await users_service.get_user(filters = filters)

        if not result:
            return {
                "message": f"User Not Found",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        
        return result
    except Exception as error:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"API Error: {str(error)}"
        )