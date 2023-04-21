import pytest

from app.utils.error import create_error_response

pytestmark = pytest.mark.asyncio


class TestErrorMsg:

    async def test_101_error(self):
        result = await create_error_response(101)
        assert not result.result
        assert result.error_type == "Not Found"
        assert result.error_message == "No user found with such id!"

    async def test_102_error(self):
        result = await create_error_response(102)
        assert not result.result
        assert result.error_type == "Bad Request"
        assert result.error_message == "It is unable to perform such operation on your own account!"

    async def test_103_error(self):
        result = await create_error_response(103)
        assert not result.result
        assert result.error_type == "Bad Request"
        assert result.error_message == "You already follow this user!"

    async def test_104_error(self):
        result = await create_error_response(104)
        assert not result.result
        assert result.error_type == "Not Found"
        assert result.error_message == "No tweet found with such id!"

    async def test_105_error(self):
        result = await create_error_response(105)
        assert not result.result
        assert result.error_type == "Not Authorized"
        assert result.error_message == "You are unable to delete tweet, created by another user!"

    async def test_106_error(self):
        result = await create_error_response(106)
        assert not result.result
        assert result.error_type == "Bad Request"
        assert result.error_message == "You are unable to like/unlike your own tweet!"

    async def test_107_error(self):
        result = await create_error_response(107)
        assert not result.result
        assert result.error_type == "Bad Request"
        assert result.error_message == "You are unable to unlike tweet, you don't like!"

    async def test_108_error(self):
        result = await create_error_response(108)
        assert not result.result
        assert result.error_type == "Bad Request"
        assert result.error_message == "Uploaded file is not an image!"

    async def test_109_error(self):
        result = await create_error_response(109)
        assert not result.result
        assert result.error_type == "Bad Request"
        assert result.error_message == "Wrong number of the tweet images!"
