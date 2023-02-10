from fastapi import Header, HTTPException, Depends

from app.db.repositories.users import UserCRUD
from app.db.dependencies import get_user_crud


user_crud = Depends(get_user_crud)


async def is_authenticate(x_token: str = Header(default=None),
                          user_crud: UserCRUD = user_crud):
    # if x_token != "Superior":
    if not await user_crud.get_by_apikey(x_token):
        raise HTTPException(status_code=403, detail="Not authorized!")
