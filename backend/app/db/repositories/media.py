from typing import List, Optional

from sqlalchemy import Column, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import Media
from app.models.media import MediaCreate, MediaInDB


class MediaCRUD:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upload_image(self, media: MediaCreate) -> MediaInDB:
        input_data = media.dict()
        new_media = Media(**input_data)
        self.session.add(new_media)
        await self.session.commit()
        dot_idx = new_media.link.rfind(".")  # type: ignore
        new_media.link = f"image{new_media.id}"  # type: ignore
        if dot_idx != -1:
            new_media.link += media.link[dot_idx:]  # type: ignore
        await self.session.commit()
        return MediaInDB.from_orm(new_media)

    async def link_images_to_tweet(self, tweet_id: int, media_ids: List[int]) -> None:
        update_stm = (
            update(Media).where(Media.id.in_(media_ids)).values(tweet_id=tweet_id)
        )
        await self.session.execute(update_stm)
        await self.session.commit()

    async def get_images_by_tweet(self, tweet_id: int) -> List[Column[str]]:
        select_stm = select(Media).where(Media.tweet_id == tweet_id)
        query_result = await self.session.execute(select_stm)
        images_list = list()
        for item in query_result.scalars().all():
            images_list.append(item.link)
        return images_list

    async def check_images_exist(self, media_ids: List[int]) -> bool:
        select_stm = (
            select(func.count(Media.id))
            .select_from(Media)
            .where(Media.id.in_(media_ids))
            .where(Media.tweet_id == None)
        )
        query_result = await self.session.execute(select_stm)
        return query_result.scalars().first() == len(media_ids)

    async def tweet_images_count(self, tweet_id: int) -> Optional[int]:
        select_stm = (
            select(func.count(Media.id))
            .select_from(Media)
            .where(Media.tweet_id == tweet_id)
        )
        query_result = await self.session.execute(select_stm)
        return query_result.scalars().first()
