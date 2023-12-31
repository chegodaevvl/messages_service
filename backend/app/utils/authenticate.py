from fastapi import Depends, Header, HTTPException

from app.db.dependencies import get_user_crud
from app.db.repositories.users import UserCRUD

user_crud = Depends(get_user_crud)


async def is_authenticate(
    api_key: str = Header(default=None), user_crud: UserCRUD = user_crud
):
    """
    Функция проверки возможности пользователя получить доступ к api
    :param api_key: str - api_key для доступа к выполнению api
    :param user_crud: CRUD операции для пользователя
    :return: Exceotion 403 - Not Authorized
    """
    if not await user_crud.get_by_apikey(api_key):
        raise HTTPException(status_code=403, detail="Not authorized!")
