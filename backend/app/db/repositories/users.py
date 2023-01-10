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

CREATE_USER = """
    INSERT INTO users (name, access_key)
    VALUES (:name, :access_key)
    RETURNING id, name, access_key;
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

    async def create_user(self, *, new_user) -> UserInDB:
        query_value = new_user.dict()

        user = await self.db.fetch_one(query=CREATE_USER, values=query_value)
        return UserInDB(**user)
