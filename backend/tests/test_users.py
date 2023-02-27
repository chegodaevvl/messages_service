import pytest

from httpx import AsyncClient
from fastapi import FastAPI


from starlette.status import HTTP_404_NOT_FOUND

pytestmark = pytest.mark.asyncio

class TestUserRoutes:

    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("tweets:create-tweet"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND
