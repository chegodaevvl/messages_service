from os import makedirs, path
from typing import Union

from fastapi import APIRouter, Depends, UploadFile, status, Request, Form

from app.core.settings import settings
from app.db.dependencies import get_media_crud
from app.db.repositories.media import MediaCRUD
from app.models.error import ErrorResponse
from app.models.media import MediaCreate
from app.models.response import MediaResponse
from app.utils.error import create_error_response

router = APIRouter()


media_crud = Depends(get_media_crud)


@router.post(
    "",
    response_model=MediaResponse,
    response_model_exclude_unset=True,
    name="medias:add-media",
    status_code=status.HTTP_200_OK,
)
async def upload_media(
    file: UploadFile,
    request: Request,
    # file = Form(),
    media_crud: MediaCRUD = media_crud,
) -> Union[MediaResponse, ErrorResponse]:
    """
    Маршрут для загрузки изображения
    :param image: файл для загрузки
    :param media_crud: CRUD для работы с изображениями
    :return: Информация о выполнении операции
    """
    if "image" not in str(file.content_type):
        return await create_error_response(108)
    new_media = MediaCreate(link=str(file.filename))
    media_uploaded = await media_crud.upload_image(new_media)
    if not path.exists(settings.MEDIA_PATH):
        makedirs(settings.MEDIA_PATH)
    with open(
        path.join(settings.MEDIA_PATH, media_uploaded.link), "wb"
    ) as uploaded_image:
        uploaded_image.write(file.file.read())
    return MediaResponse(
        result=True,
        media_id=media_uploaded.id,
        error_type=None,
        error_message=None,
    )
