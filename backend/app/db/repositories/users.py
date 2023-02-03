from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert

from app.db.models import User


class UserCRUD:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_secret(self, secret: str):
        select_stm = select(User).where(User.api_key == secret)
        result = await self.session.execute(select_stm)
        return result.scalars().all()

    async def bulk_add(self, users: list) -> None:
        add_stm = insert(User).values(users)
        await self.session.execute(add_stm)
        await self.session.commit()
