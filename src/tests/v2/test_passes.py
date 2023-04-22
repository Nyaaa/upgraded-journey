import os

import pytest
from fastapi import HTTPException, UploadFile
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import schemas, models
from app.api.v2 import routes
from tests.sample_data import COORDS, BIN_FILE, PASSAGE

URL = "/v2/passages/"


@pytest.mark.asyncio
async def test_pass_get_all(client: AsyncClient, create_passage: models.Passage):
    response = await client.get(URL)
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_pass_post_no_image(
    async_session: AsyncSession, create_user: models.User
):
    passage = schemas.PassageBase(**PASSAGE)
    coords = schemas.Coords(**COORDS)
    response = await routes.create_passage(
        passage=passage, coords=coords, db=async_session, user=create_user
    )

    assert response.id == 1
    assert response.status == "new"


@pytest.mark.asyncio
async def test_pass_post_with_image(
    async_session: AsyncSession, create_user: models.User
):
    passage = schemas.PassageBase(**PASSAGE)
    coords = schemas.Coords(**COORDS)
    response = await routes.create_passage(
        passage=passage,
        coords=coords,
        image_title=["image_title1,image_title2"],
        image_file=[
            UploadFile(file=BIN_FILE, filename="test"),
            UploadFile(file=BIN_FILE, filename="test"),
        ],
        db=async_session,
        user=create_user,
    )
    assert len(response.images) == 2
    for image in response.images:
        assert os.path.isfile(image.filepath)


@pytest.mark.asyncio
async def test_passes_get_one(
    async_session: AsyncSession, create_passage: models.Passage
):
    response = await routes.read_passage_by_id(db=async_session, passage_id=1)
    assert response.id == 1


@pytest.mark.asyncio
async def test_passage_not_found(async_session: AsyncSession):
    with pytest.raises(HTTPException) as err:
        await routes.read_passage_by_id(db=async_session, passage_id=10)
    assert err.value.status_code == 404
    assert err.value.detail == {"status": 404, "message": "Passage not found"}
