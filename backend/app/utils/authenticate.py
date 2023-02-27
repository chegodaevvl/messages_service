from app.db.repositories.users import UserCRUD


async def is_authenticate(api_key: str, user_crud: UserCRUD) -> bool:
    if not await user_crud.get_by_apikey(api_key):
        return False
    return True
