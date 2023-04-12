from app.models.core import CoreModel, IDModelMixin


class MediaBase(CoreModel):
    link: str


class MediaCreate(MediaBase):
    pass


class MediaInDB(IDModelMixin, MediaBase):
    pass

    class Config:
        orm_mode = True
