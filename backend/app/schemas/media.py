from app.schemas.core import CoreModel, IDModelMixin


class MediaBase(CoreModel):
    """
    Модель описания изображения
    """

    link: str


class MediaCreate(MediaBase):
    """
    Модель для создания изображения
    """

    pass


class MediaInDB(IDModelMixin, MediaBase):
    """
    Модель хранения изображения в БД
    """

    pass

    class Config:
        orm_mode = True
