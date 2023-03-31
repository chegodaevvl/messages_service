import pytest

from httpx import AsyncClient

from fastapi import status


pytestmark = pytest.mark.asyncio


class TestMedia:

    async def test_upload_media(self,
                                client: AsyncClient,
                                test_user) -> None:
        image_file = "image.jpeg"
        path_to_file = "tests/image.jpeg"
        images = {
            "image": open(path_to_file, "rb")
        }
        result = await client.post("api/media", headers={"api-key": test_user.api_key}, files=images)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert response["media_id"] == 1
