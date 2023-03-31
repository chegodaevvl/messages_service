from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Media
from app.models.media import MediaCreate, MediaInDB


class MediaCRUD:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upload_image(self, media: MediaCreate) -> MediaInDB:
        new_media = Media(**media)
        self.session.add(new_media)
        await self.session.commit()
        return MediaInDB.from_orm(new_media)
