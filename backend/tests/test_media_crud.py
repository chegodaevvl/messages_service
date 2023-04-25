import pytest

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.media import MediaCRUD
from app.db.models import Media
from app.models.media import MediaCreate


pytestmark = pytest.mark.asyncio


class TestMediaCRUD:

    async def test_media_upload_image(
            self,
            db: AsyncSession
    ) -> None:
        media_crud = MediaCRUD(db)
        new_media = MediaCreate(
            link="test_image.jpg"
        )
        media_uploaded = await media_crud.upload_image(new_media)
        assert media_uploaded.link == f"image{media_uploaded.id}.jpg"
        new_media = MediaCreate(
            link="test_image"
        )
        media_uploaded = await media_crud.upload_image(new_media)
        assert media_uploaded.link == f"image{media_uploaded.id}"
        delete_stm = delete(Media)
        await db.execute(delete_stm)
        await db.commit()

    async def test_check_images_exist(self,
                                      db: AsyncSession,
                                      first_tweet):
        media_crud = MediaCRUD(db)
        media_ids = list()
        for i in range(2):
            new_media = MediaCreate(
                link="test_image.jpg"
            )
            media_uploaded = await media_crud.upload_image(new_media)
            media_ids.append(media_uploaded.id)
        result = await media_crud.check_images_exist(media_ids)
        assert result
        await media_crud.link_images_to_tweet(first_tweet.id, media_ids)
        result = await media_crud.check_images_exist(media_ids)
        assert not result
        delete_stm = delete(Media)
        await db.execute(delete_stm)
        await db.commit()

    async def test_tweet_images_count(self,
                                      db: AsyncSession,
                                      first_tweet):
        media_crud = MediaCRUD(db)
        media_ids = list()
        for i in range(2):
            new_media = MediaCreate(
                link="test_image.jpg"
            )
            media_uploaded = await media_crud.upload_image(new_media)
            media_ids.append(media_uploaded.id)
        await media_crud.link_images_to_tweet(first_tweet.id, media_ids)
        media_count = await media_crud.tweet_images_count(first_tweet.id)
        assert media_count == len(media_ids)
        delete_stm = delete(Media)
        await db.execute(delete_stm)
        await db.commit()
