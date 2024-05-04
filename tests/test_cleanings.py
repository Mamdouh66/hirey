import pytest

from typing import AsyncGenerator

from fastapi import FastAPI, status
from async_asgi_testclient import TestClient


class TestCleaningsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(
        self, app: FastAPI, client: AsyncGenerator[TestClient, None]
    ) -> None:
        async for test_client in client:
            res = await test_client.post(
                app.url_path_for("cleanings:create-cleaning"), json={}
            )
            assert res.status_code != status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncGenerator[TestClient, None]
    ) -> None:
        async for test_client in client:
            res = await test_client.post(
                app.url_path_for("cleanings:create-cleaning"), json={}
            )
            assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
