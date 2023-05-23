from os import path, remove
import pytest

from httpx import AsyncClient

from fastapi import status
from app.core.settings import settings

pytestmark = pytest.mark.asyncio


class TestMedia:

    async def test_upload_media(self,
                                client: AsyncClient,
                                first_user) -> None:
        path_to_file = "tests/image.jpeg"
        images = {
            "file": open(path_to_file, "rb")
        }
        result = await client.post("api/medias", headers={"api-key": first_user.api_key}, files=images)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"]
        assert response["media_id"] == 1
        assert path.exists(path.join(settings.MEDIA_PATH, f"image{response['media_id']}.jpeg"))
        remove(path.join(settings.MEDIA_PATH, f"image{response['media_id']}.jpeg"))

    async def test_upload_wrong_media(self,
                                      client: AsyncClient,
                                      first_user) -> None:
        path_to_file = "tests/text.txt"
        images = {
            "file": open(path_to_file, "rb")
        }
        result = await client.post("api/medias", headers={"api-key": first_user.api_key}, files=images)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        print(response.keys())
        assert not response["result"]
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "Uploaded file is not an image!"
