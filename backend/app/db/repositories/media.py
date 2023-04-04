from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update

from app.db.models import Media
from app.models.media import MediaCreate, MediaInDB


class MediaCRUD:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upload_image(self, media: MediaCreate) -> MediaInDB:
        new_media = Media(**media)
        self.session.add(new_media)
        await self.session.commit()
        dot_idx = new_media.file.rfind(".")
        new_media.file = f"image{new_media.id}"
        if dot_idx != -1:
            new_media.file += media["file"][dot_idx:]
        # await self.session.commit()
        return MediaInDB.from_orm(new_media)

    async def delete_images(self, tweet_id: int) -> None:
        delete_stm = delete(Media).where(
            Media.tweet_id == tweet_id
        )
        await self.session.execute(delete_stm)
        await self.session.commit()

    async def link_images_to_tweet(self, tweet_id: int, media_ids: List[int]) -> None:
        update_stm = update(Media).where(
            Media.id.in_(media_ids)
        ).values(tweet_id=tweet_id)
        await self.session.execute(update_stm)
        await self.session.commit()

    async def get_images_by_tweet(self, tweet_id: int) -> List[str]:
        select_stm = select(Media).where(
            Media.tweet_id == tweet_id
        )
        query_result = await self.session.execute(select_stm)
        images_list = list()
        for item in query_result.scalars().all():
            images_list.append(item.file)
        return images_list

    async def check_images_exist(self, media_ids: List[int]) -> bool:
        select_stm = select(Media).where(
            Media.id.in_(media_ids)
        )
        query_result = await self.session.execute(select_stm)
        return len(query_result.scalars().all()) == len(media_ids)
