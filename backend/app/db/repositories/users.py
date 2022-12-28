from app.db.repositories.base import BaseRepository
from app.models.users import UserBase, UserInDB, UserPublic


GET_USER_BY_ID = """
    SELECT id, name
    FROM users
    WHERE id = :id;
"""

GET_USER_BY_SECRET = """
    SELECT id, name
    FROM users
    WHERE access_key = :secret;
"""


class UserRepository(BaseRepository):

    async def get_user_by_id(self, *, id: int) -> UserInDB:
        user = await self.db.fetch_one(query=GET_USER_BY_ID, values={"id": id})

        if not user:
            return user

        return UserInDB(**user)

    async def get_user_by_secret(self, *, secret: str) -> UserInDB:
        user = await self.db.fetch_one(query=GET_USER_BY_SECRET, values={"secret": secret})

        if not user:
            return user

        return UserInDB(**user)
